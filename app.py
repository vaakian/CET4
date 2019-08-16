from flask_restful import Api, Resource
from flask import Flask, request, render_template
import requests
session = requests.session()
session.headers = {'Referer': 'http://cache.neea.edu.cn/'}

class STUDENT:
		def __init__(self, num, name):
				self.ver_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik=' + \
						num + '&t=0.8030510069176611'
				self.num = num
				self.name = name

		def get_ver_img(self):
				ver_code = session.get(self.ver_url)
				ver_code = ver_code.text[13:-3]
				ver_img = 'http://cet.neea.edu.cn/imgs/' + ver_code + '.png'
				return ver_img

		def get_score(self, DANGCI, v):
				# http://cache.neea.edu.cn/cet/query?data=CET4_191_DANGCI,420640191107626,熊维建&v=yfp5
				params = {
						'data': '{},{},{}'.format(DANGCI, self.num, self.name),
						'v': v
				}
				try:
						res = session.get(
								url='http://cache.neea.edu.cn/cet/query', params=params)
						return res.text
				except Exception as e:
						return str(e)
app = Flask(__name__)
api = Api(app)
stu_list = {}


class SCORE(Resource):
		def get(self):	# 返回验证码, 此时创建对象
				num = request.args.get('num')
				name = request.args.get('name')
				stu_list[num] = STUDENT(num, name)
				stu = stu_list[num]
				ver_img = stu.get_ver_img()
				return {'url': ver_img}

		def post(self):
				data = request.json
				num = data['num']
				name = data['name']
				dangci = data['dangci']
				v = data['v']
				stu = stu_list[num]
				score = stu.get_score(dangci, v)
				del stu	# 释放对象
				del stu_list[num]	# 删除记录
				return score[:-2].replace('result.callback(', '')

# 输入用户名账号-》请求验证码-》创建stu对象-》请求成绩使用已创建好的对象
api.add_resource(SCORE, '/score')


@app.route('/')
def index():
  	return render_template('index.html')
if __name__ == '__main__':
		app.run(debug=False, port=86, host='0.0.0.0')
