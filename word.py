#coding:utf-8
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
import codecs
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sys,getopt
opts,args=getopt.getopt(sys.argv[1:],"ht:i:f:o:",["input_text_file","input_image_file","font_file","out_file"])
input_text_file=""
input_image_file=""
out_file=""
font_file=""
USAGE='''
	This script generate word cloud given an text file and an image file
	usage: python word.py -t <input_text_file> -i <input_image_file> -o <out_file>
		required argument:
			-t | --input_text_file : input file in text
			-i | --input_image_file: input image file
			-f | --font_file: font file
			-o | --out_file : output file prefix
'''
for opt,value in opts:
	if opt =="h":
		print USAGE
		sys.exit(2)
	elif opt in ("-t","--input_text_file"):
		input_text_file=value
	elif opt in ("-i","--input_image_file"):
		input_image_file=value
	elif opt in ("-f","--font_file"):
		font_file=value
	elif opt in ("-o","--out_file"):
		out_file =value
 
	
#print coverage
if (input_text_file=="" or input_image_file=="" or out_file ==""):
	print USAGE
	sys.exit(2)

stopwords = {}
def importStopword(filename=''):
    global stopwords
    f = codecs.open(filename, 'r', encoding='utf-8')
    line = f.readline().rstrip()

    while line:
        stopwords.setdefault(line, 0)
        stopwords[line] = 1
        line = f.readline().rstrip()

    f.close()

def processChinese(text):
    seg_generator = jieba.cut(text)  # 使用结巴分词，也可以不使用

    seg_list = [i for i in seg_generator if i not in stopwords]

    seg_list = [i for i in seg_list if i != u' ']

    seg_list = r' '.join(seg_list)

    return seg_list


importStopword(filename='./stopwords.txt')


# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

text = codecs.open(path.join(d, input_text_file),encoding ='utf-8').read()

#如果是中文
text = processChinese(text)#中文不好分词，使用Jieba分词进行

# read the mask / color image
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
# 设置背景图片
back_coloring = imread(path.join(d, input_image_file))
if font_file=="":
	path_font_tff='./font/叶立群几何体.ttf'
else:
	path_font_tff=font_file
wc = WordCloud( font_path=path_font_tff,#设置字体
                background_color="black", #背景颜色
                max_words=2000,# 词云显示的最大词数
                mask=back_coloring,#设置背景图片
                #max_font_size=100, #字体最大值
                random_state=42,
                )
# 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(back_coloring)

plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
#plt.show()
# 绘制词云
'''plt.figure()


# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")


# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
'''
# 保存图片
wc.to_file(path.join(d, out_file+".png"))
