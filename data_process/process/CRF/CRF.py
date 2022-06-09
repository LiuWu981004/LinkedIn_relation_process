def compute_score(emissions, tags, seq_ends, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # tags: (seq_length, batch_size)
    # mask: (seq_length, batch_size)

    seq_length, batch_size = tags.shape
    mask = mask.astype(emissions.dtype)

    # 将score设置为初始转移概率
    # shape: (batch_size,)
    score = start_trans[tags[0]]
    # score += 第一次发射概率
    # shape: (batch_size,)
    score += emissions[0, mnp.arange(batch_size), tags[0]]

    for i in range(1, seq_length):
        # 标签由i-1转移至i的转移概率（当mask == 1时有效）
        # shape: (batch_size,)
        score += trans[tags[i - 1], tags[i]] * mask[i]

        # 预测tags[i]的发射概率（当mask == 1时有效）
        # shape: (batch_size,)
        score += emissions[i, mnp.arange(batch_size), tags[i]] * mask[i]

    # 结束转移
    # shape: (batch_size,)
    last_tags = tags[seq_ends, mnp.arange(batch_size)]
    # score += 结束转移概率
    # shape: (batch_size,)
    score += end_trans[last_tags]

    return score


def compute_normalizer(emissions, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # mask: (seq_length, batch_size)

    seq_length = emissions.shape[0]

    # 将score设置为初始转移概率，并加上第一次发射概率
    # shape: (batch_size, num_tags)
    score = start_trans + emissions[0]

    for i in range(1, seq_length):
        # 扩展score的维度用于总score的计算
        # shape: (batch_size, num_tags, 1)
        broadcast_score = score.expand_dims(2)

        # 扩展emission的维度用于总score的计算
        # shape: (batch_size, 1, num_tags)
        broadcast_emissions = emissions[i].expand_dims(1)

        # 根据公式(7)，计算score_i
        # 此时broadcast_score是由第0个到当前Token所有可能路径
        # 对应score的log_sum_exp
        # shape: (batch_size, num_tags, num_tags)
        next_score = broadcast_score + trans + broadcast_emissions

        # 对score_i做log_sum_exp运算，用于下一个Token的score计算
        # shape: (batch_size, num_tags)
        next_score = mnp.log(mnp.sum(mnp.exp(next_score), axis=1))

        # 当mask == 1时，score才会变化
        # shape: (batch_size, num_tags)
        score = mnp.where(mask[i].expand_dims(1), next_score, score)

    # 最后加结束转移概率
    # shape: (batch_size, num_tags)
    score += end_trans
    # 对所有可能的路径得分求log_sum_exp
    # shape: (batch_size,)
    return mnp.log(mnp.sum(mnp.exp(score), axis=1))


def viterbi_decode(emissions, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # mask: (seq_length, batch_size)

    seq_length = mask.shape[0]

    score = start_trans + emissions[0]
    history = ()

    for i in range(1, seq_length):
        broadcast_score = score.expand_dims(2)
        broadcast_emission = emissions[i].expand_dims(1)
        next_score = broadcast_score + trans + broadcast_emission

        # 求当前Token对应score取值最大的标签，并保存
        indices = next_score.argmax(axis=1)
        history += (indices,)

        next_score = next_score.max(axis=1)
        score = mnp.where(mask[i].expand_dims(1), next_score, score)

    score += end_trans

    return score, history


def post_decode(score, history, seq_length):
    # 使用Score和History计算最佳预测序列
    batch_size = seq_length.shape[0]
    seq_ends = seq_length - 1
    # shape: (batch_size,)
    best_tags_list = []

    # 依次对一个Batch中每个样例进行解码
    for idx in range(batch_size):
        # 查找使最后一个Token对应的预测概率最大的标签，
        # 并将其添加至最佳预测序列存储的列表中
        best_last_tag = score[idx].argmax(axis=0)
        best_tags = [int(best_last_tag.asnumpy())]
        #
        # 重复查找每个Token对应的预测概率最大的标签，加入列表
        for hist in reversed(history[:seq_ends[idx]]):
            best_last_tag = hist[idx][best_tags[-1]]
            best_tags.append(int(best_last_tag.asnumpy()))

        # 将逆序求解的序列标签重置为正序
        best_tags.reverse()
        best_tags_list.append(best_tags)

    return best_tags_list


import mindspore
import mindspore.nn as nn
import mindspore.numpy as mnp
from mindspore import Parameter
from mindspore.common.initializer import initializer, Uniform


def sequence_mask(seq_length, max_length, batch_first=False):
    """根据序列实际长度和最大长度生成mask矩阵"""
    range_vector = mnp.arange(0, max_length, 1, seq_length.dtype)
    result = range_vector < seq_length.view(seq_length.shape + (1,))
    if batch_first:
        return result.astype(mindspore.int64)
    return result.astype(mindspore.int64).swapaxes(0, 1)


class CRF(nn.Cell):
    def __init__(self, num_tags: int, batch_first: bool = False, reduction: str = 'sum') -> None:
        if num_tags <= 0:
            raise ValueError(f'invalid number of tags: {num_tags}')
        super().__init__()
        if reduction not in ('none', 'sum', 'mean', 'token_mean'):
            raise ValueError(f'invalid reduction: {reduction}')
        self.num_tags = num_tags
        self.batch_first = batch_first
        self.reduction = reduction
        self.start_transitions = Parameter(initializer(Uniform(0.1), (num_tags,)), name='start_transitions')
        self.end_transitions = Parameter(initializer(Uniform(0.1), (num_tags,)), name='end_transitions')
        self.transitions = Parameter(initializer(Uniform(0.1), (num_tags, num_tags)), name='transitions')


def construct(self, emissions, tags=None, seq_length=None):
    if tags is None:
        return self._decode(emissions, seq_length)
    return self._forward(emissions, tags, seq_length)


def _forward(self, emissions, tags=None, seq_length=None):
    if self.batch_first:
        batch_size, max_length = tags.shape
        emissions = emissions.swapaxes(0, 1)
        tags = tags.swapaxes(0, 1)
    else:
        max_length, batch_size = tags.shape

    if seq_length is None:
        seq_length = mnp.full((batch_size,), max_length, mindspore.int64)

    mask = sequence_mask(seq_length, max_length)

    # shape: (batch_size,)
    numerator = compute_score(emissions, tags, seq_length - 1, mask, self.transitions, self.start_transitions,
                              self.end_transitions)
    # shape: (batch_size,)
    denominator = compute_normalizer(emissions, mask, self.transitions, self.start_transitions,
                                     self.end_transitions)
    # shape: (batch_size,)
    llh = denominator - numerator

    if self.reduction == 'none':
        return llh
    elif self.reduction == 'sum':
        return llh.sum()
    elif self.reduction == 'mean':
        return llh.mean()
    return llh.sum() / mask.astype(emissions.dtype).sum()


def _decode(self, emissions, seq_length=None):
    if self.batch_first:
        batch_size, max_length = emissions.shape[:2]
        emissions = emissions.swapaxes(0, 1)
    else:
        batch_size, max_length = emissions.shape[:2]

    if seq_length is None:
        seq_length = mnp.full((batch_size,), max_length, mindspore.int64)

    mask = sequence_mask(seq_length, max_length)

    return viterbi_decode(emissions, mask, self.transitions, self.start_transitions, self.end_transitions)


class BiLSTM_CRF(nn.Cell):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_tags, padding_idx=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2, bidirectional=True, batch_first=True)
        self.hidden2tag = nn.Dense(hidden_dim, num_tags, 'he_uniform')
        self.crf = CRF(num_tags, batch_first=True)

    def construct(self, inputs, seq_length, tags=None):
        embeds = self.embedding(inputs)
        outputs, _ = self.lstm(embeds, seq_length=seq_length)
        feats = self.hidden2tag(outputs)

        crf_outs = self.crf(feats, tags, seq_length)
        return crf_outs


embedding_dim = 5
hidden_dim = 4

training_data = [(
    "清 华 大 学 坐 落 于 首 都 北 京".split(),
    "B I I I O O O O O B I".split()
), (
    "重 庆 是 一 个 魔 幻 城 市".split(),
    "B I O O O O O O O".split()
)]

word_to_idx = {}
word_to_idx['<pad>'] = 0
for sentence, tags in training_data:
    for word in sentence:
        if word not in word_to_idx:
            word_to_idx[word] = len(word_to_idx)

tag_to_idx = {"B": 0, "I": 1, "O": 2}


def prepare_sequence(seqs, word_to_idx, tag_to_idx):
    seq_outputs, label_outputs, seq_length = [], [], []
    max_len = max([len(i[0]) for i in seqs])

    for seq, tag in seqs:
        seq_length.append(len(seq))
        idxs = [word_to_idx[w] for w in seq]
        labels = [tag_to_idx[t] for t in tag]
        idxs.extend([word_to_idx['<pad>'] for i in range(max_len - len(seq))])
        labels.extend([tag_to_idx['O'] for i in range(max_len - len(seq))])
        seq_outputs.append(idxs)
        label_outputs.append(labels)

    return mindspore.Tensor(seq_outputs, mindspore.int64), \
           mindspore.Tensor(label_outputs, mindspore.int64), \
           mindspore.Tensor(seq_length, mindspore.int64)


data, label, seq_length = prepare_sequence(training_data, word_to_idx, tag_to_idx)

from tqdm import tqdm

train_one_step.compile(data, seq_length, label)

steps = 500
with tqdm(total=steps) as t:
    for i in range(steps):
        loss = train_one_step(data, seq_length, label)
        t.set_postfix(loss=loss)
        t.update(1)

idx_to_tag = {idx: tag for tag, idx in tag_to_idx.items()}

def sequence_to_tag(sequences, idx_to_tag):
    outputs = []
    for seq in sequences:
        outputs.append([idx_to_tag[i] for i in seq])
    return outputs

sequence_to_tag(predict, idx_to_tag)