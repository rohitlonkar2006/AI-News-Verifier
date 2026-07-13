import re
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            name="attention_weight",
            shape=(input_shape[-1], input_shape[-1]),
            initializer="glorot_uniform",
            trainable=True
        )

        self.b = self.add_weight(
            name="attention_bias",
            shape=(input_shape[-1],),
            initializer="zeros",
            trainable=True
        )

        self.u = self.add_weight(
            name="context_vector",
            shape=(input_shape[-1], 1),
            initializer="glorot_uniform",
            trainable=True
        )
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        score = tf.tanh(
            tf.tensordot(x, self.W, axes=1) + self.b
        )

        attention_weights = tf.nn.softmax(
            tf.tensordot(score, self.u, axes=1),
            axis=1
        )

        context_vector = tf.reduce_sum(
            attention_weights * x,
            axis=1
        )
        return context_vector

    def get_config(self):
        config = super(AttentionLayer, self).get_config()
        return config

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_inputs(title, article, tokenizer, title_max_len, text_max_len):
    title = clean_text(title)
    article = clean_text(article)

    title_seq = tokenizer.texts_to_sequences([title])
    text_seq = tokenizer.texts_to_sequences([article])

    title_pad = pad_sequences(
        title_seq,
        maxlen=title_max_len,
        padding="post",
        truncating="post"
    )

    text_pad = pad_sequences(
        text_seq,
        maxlen=text_max_len,
        padding="post",
        truncating="post"
    )

    return title_pad, text_pad