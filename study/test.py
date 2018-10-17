
import  tensorflow as tf

s = tf.constant('hello')
sess = tf.Session()

print(sess.run(s))