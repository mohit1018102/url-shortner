from flask import render_template, request, redirect, url_for,flash, abort,session,jsonify,Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

ip="http://192.168.0.109:5000/"
bp=Blueprint('urlshort',__name__)

@bp.route('/') #  home page
def home():
    return render_template("home.html",codes=session.keys())



@bp.route('/your-url',methods=['POST','GET']) #  about page
def your_url():
    if request.method =='POST':
        urls ={}
        # if file exists --> load the data to local dictionary
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)

        # check if key exits
        if request.form['code'] in urls.keys():
            # send message to next page for printing Alters
            flash(f'{request.form['code']} short name has already been taken, please select another name!!')

            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            f=request.files['file']
            # bad intention name can be avoided using secure_filename.
            # to check it is safe to save.
            # to avoid name collision
            full_name=request.form['code'] + secure_filename(f.filename)
            f.save('./urlshort/static/files/'+full_name)
            urls[request.form['code']]={'file':full_name}

        with open('urls.json','w') as url_files:
            json.dump(urls,url_files)
            session[ip+request.form['code']] = True
        return render_template("your_url.html",code=request.form['code'],site_prefix=ip)
    else:
        #return render_template("your_url.html",code=request.args['code']) for get
        # return render_template("home.html")
        # instead of render new template we redirect to the home page
        # render : result in url /your-url but redirect : /
        #return redirect('/') # if home url change we have to made in multiple places. better use
        return redirect(url_for('urlshort.home')) # independent of home page url


# redirect
# it says any string after / save it code
@bp.route('/<string:code>') #  home page
def redirect_to_url(code):
    urls={}
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls=json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    # static : icon, css, logo, used to store userfiles
                    return redirect(url_for('static',filename='files/'+urls[code]['file']))

    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

if __name__ == '__main__':
    app.run(debug=True)
