from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import short_url
import validators
import re

app = Flask(__name__)
api = Api(app)


# url_mapping={ 'index1' : {'original_url' : 'google.com' ,'url_id': 'g.com'},
#               'index2' : {'original_url' : 'google.nl' ,'url_id': 'g.nl'} }
url_mapping={}

parser = reqparse.RequestParser()
parser.add_argument('original_url')
parser.add_argument('url_id')

def IsExist(original_url):
    for item in url_mapping:
                for urls in url_mapping[item]:
                    if urls=='original_url' and url_mapping[item][urls] == original_url : 
                        return url_mapping[item]['url_id']
    return "not found"


class ShortURL(Resource):
    def get(self,url_id):
        for item in url_mapping:
            for urls in url_mapping[item]:
                if urls=='url_id' and url_mapping[item][urls] == url_id : 
                    return url_mapping[item]['original_url'],301
        abort(404)
        #return 404

    def put(self,url_id):
        found=0
        matched=re.match("^[A-Za-z0-9_-]*$", url_id)
        if matched:
            for item in url_mapping:
                for urls in url_mapping[item]:
                    if urls=='url_id' and url_mapping[item][urls] == url_id : 
                        found=1
            if found:
                return '',200
            else:
                abort(404)
        else:
            abort(400,message="error")
        
        # abort(404, message='URL {} doesnot exist'.format(short_url))

    def delete(self,url_id):
        for item in url_mapping:
            for urls in url_mapping[item]:
                if urls=='url_id' and url_mapping[item][urls] == url_id : 
                    del url_mapping[item]
                    return '',204
        abort(404)
        
class OriginalURL(Resource):
    def get(self):
        all_urls=[]
        for item in url_mapping:
            for urls in url_mapping[item]:
                if urls=='original_url':
                    all_urls.append(url_mapping[item][urls])
        return all_urls,200

    def post(self):
        args=parser.parse_args()
        if len(url_mapping)==0:
            index=1
        else:
            index=int(max(url_mapping.keys()).lstrip('index')) + 1

        found=IsExist(args['original_url'])
        if found!="not found":
            return found,201

        validate=validators.url(args['original_url'])
        if validate!=True:
           abort(400,message='error') 

        url_id=short_url.encode_url(index)
        index = 'index%i' % index
        url_mapping[index]={'original_url':args['original_url'],'url_id':url_id}
        return url_id,201
        abort(400,message='error')

    def delete(self):
       url_mapping.clear()
       return '',204     
        

api.add_resource(ShortURL, '/<url_id>')
api.add_resource(OriginalURL, '/')


if __name__ == '__main__':
    app.run(debug=True)