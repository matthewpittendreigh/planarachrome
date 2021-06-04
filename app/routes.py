import os
import numpy
import csv
import time
import configparser
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, flash, make_response, jsonify
from werkzeug.utils import secure_filename

from app import app
from app.create_display import *
from app.detect_edge import *
from app.quantify import *

# Index: Image upload and project select screen


@app.route('/')
# @app.route('/index')
def index():
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    if not os.path.isdir(display_dir):
        os.mkdir(display_dir)
    else:
        print('Directory exists: {}'.format(display_dir))
    files = os.listdir(display_dir)
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    upload_dir = os.path.join(app.config['UPLOAD_PATH'], 'uploads/')
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    else:
        print('Directory exists: {}'.format(upload_dir))

    for uploaded_file in request.files.getlist('file'):
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            print(file_ext)
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(upload_dir, filename))

            if file_ext == '.tif':
                tif_save_png(upload_dir, filename, display_dir, addtime=False)
            elif file_ext == '.png':
                png_save_png(upload_dir, filename, display_dir, addtime=False)
             
    return redirect(url_for('index'))


@app.route('/delete', methods=["POST"])
def delete_files():
    upload_dir = os.path.join(app.config['UPLOAD_PATH'], 'uploads/')
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')

    existing_files = os.listdir(upload_dir)
    for upload_filename in existing_files:
        os.remove(os.path.join(upload_dir, upload_filename))

    existing_files = os.listdir(display_dir)
    for display_filename in existing_files:
        os.remove(os.path.join(display_dir, display_filename))

    existing_files = os.listdir(mask_dir)
    for mask_filename in existing_files:
        os.remove(os.path.join(mask_dir, mask_filename))

    return redirect(url_for('index'))


@app.route('/display/<filename>')
def display(filename):
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    return send_from_directory(display_dir, filename)

# Mask editor: Mask display, edit, and export tools


@app.route('/load', methods=["GET", "POST"])
def load_editor():
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')
    if not os.path.isdir(mask_dir):
        os.mkdir(mask_dir)
    else:
        print('Directory exists: {}'.format(mask_dir))

    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    threshold = config['user_settings']['initial_threshold']

    existing_files = os.listdir(mask_dir)
    for mask_filename in existing_files:
        os.remove(os.path.join(mask_dir, mask_filename))

    uploaded_files = os.listdir(display_dir)

    for filename in uploaded_files:
        filepath = os.path.join(display_dir, filename)
        preimage = preprocess_image(filepath)
        mask = threshflood(preimage, int(threshold))
        try:
            mask = remove_noise(mask)
        except IndexError:
            flash('Threshold is too high to be applied to all images')
            flash('Reduce and click Apply All to re-load images with new default threshold')
            #flash('No changes made')
            return redirect(url_for('mask_editor', mode="segmented"))
        segmented_image = mask_image(preimage, mask)
        save_png(segmented_image, filename, mask_dir, addtime=False)

    return redirect(url_for('mask_editor', mode='default', thresh_init=threshold))


@app.route('/editor/<mode>')
def mask_editor(mode):
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')
    files = os.listdir(mask_dir)

    resp = make_response(render_template('mask_editor.html', files=files, mode=mode))
    if mode=='default':
        thresh_init=request.args.get('thresh_init')
        resp.set_cookie('thresh_init', thresh_init)

    return resp


@app.route('/masks/<filename>')
def masks(filename):
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')
    return send_from_directory(mask_dir, filename)


@app.route("/threshold", methods=["POST"])
def threshold():
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')

    thr_slider = request.form["thr_slider"]
    print('Threshold request: ' + thr_slider)
    mask_url = request.form["slide_url"]
    print('Mask url: ' + mask_url)
    mask_queryname = os.path.basename(mask_url)
    mask_filename = mask_queryname.rsplit('?')[0]

    image_filepath = os.path.join(display_dir, mask_filename)
    mask_filepath = os.path.join(mask_dir, mask_filename)

    preimage = preprocess_image(image_filepath)
    mask = threshflood(preimage, threshold=int(thr_slider))
    try:
        mask = remove_noise(mask)
    except IndexError:
        flash('Threshold is too high')
        flash('No change made')
        return redirect(url_for('mask_editor', mode="segmented"))
        
    segmented_image = mask_image(preimage, mask)

    os.remove(mask_filepath)
    save_png(segmented_image, mask_filename, mask_dir, addtime=False)

    return redirect(url_for('mask_editor', mode="segmented"))

@app.route('/apply-init-threshold', methods=["POST"])
def apply_init_threshold():
    threshold = request.form.get('threshold_value')

    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.set('user_settings', 'initial_threshold', threshold)

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    return jsonify(200)
    

@app.route("/mode", methods=["POST"])
def change_mode():
    mode = request.form['view']
    if(mode == 'gsegmented'):
        mode = 'segmented'
    else:
        mode = 'raw'

    return redirect(url_for('mask_editor', mode=mode))

# Export results and display summary statistics


@app.route('/export', methods=["GET", "POST"])
def export_data():
    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')
    export_dir = os.path.join(app.config['UPLOAD_PATH'], 'exports/')

    if not os.path.isdir(export_dir):
        os.mkdir(export_dir)
    else:
        print('Directory exists: {}'.format(export_dir))

    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    percentile = int(config['user_settings']['pigment_percentile'])

    red_min_thresh = int(config['user_settings']['pigment_area_red_min'])
    red_max_thresh = int(config['user_settings']['pigment_area_red_max'])

    green_min_thresh = int(config['user_settings']['pigment_area_green_min'])
    green_max_thresh = int(config['user_settings']['pigment_area_green_max'])

    blue_min_thresh = int(config['user_settings']['pigment_area_blue_min'])
    blue_max_thresh = int(config['user_settings']['pigment_area_blue_max'])

    bins = int(config['user_settings']['histogram_bins'])

    files = os.listdir(mask_dir)
    if files:
        # delete/create csv file
        existing_files = os.listdir(export_dir)
        for csv_filename in existing_files:
            os.remove(os.path.join(export_dir, csv_filename))

        csv_filename = 'data' + str(time.time()) + '.csv'
        csv_filepath = os.path.join(export_dir, csv_filename)
        with open(csv_filepath, mode='w') as datafile:
            data_writer = csv.writer(datafile, delimiter=',', lineterminator='\n',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ['Filename', 'Intensity Quantification',
                      'Area Quantification', 'Percentile (Intensity)', 'Red Min (Area)',
                      'Red Max (Area)', 'Green Min (Area)', 'Green Max (Area)', 'Blue Min (Area)',
                      'Blue Max (Area)']
            data_writer.writerow(header)

            for idx, filename in enumerate(files):
                maskpath = os.path.join(mask_dir, filename)
                gimage = load_image(maskpath)
                displaypath = os.path.join(display_dir, filename)
                cimage = load_image(displaypath)
                mask = extract_mask(gimage)
                perc = quant_percentile(gimage, mask, percent=percentile)
                area, _, _, _, _ = quant_area(cimage, mask, min_otsu=[red_min_thresh, green_min_thresh, blue_min_thresh], 
                                  max_otsu=[red_max_thresh, green_max_thresh, blue_max_thresh])
                #combo = quant_pigment(perc, area)

                # ---> add logic for different export settings
                # nomalize percentile intensity values for comparison (current, may add setting)
                perc = 1 - (float(perc) / 255)

                if idx == 0:
                    row = [filename, round(perc, 2), round(area, 2), percentile, red_min_thresh, red_max_thresh,
                           green_min_thresh, green_max_thresh, blue_min_thresh, blue_max_thresh]
                else:
                    row = [filename, round(perc, 2), round(area, 2)]

                data_writer.writerow(row)
    else:
        flash('Cannot export - There is either no images, or the masks and settings have not been reviewed.')
        return redirect(url_for('index')) 

    return redirect(url_for('statistics', csv_filename=csv_filename, bins=bins))

@app.route('/data/<filename>')
def data(filename):
    export_dir = os.path.join(app.config['UPLOAD_PATH'], 'exports/')
    return send_from_directory(export_dir, filename)


# I don't like that I need to put this here to pass the csvfilename
# but it actually may be best because people will know they can't go back to 
# last exported data.
@app.route('/statistics/<csv_filename>/<bins>')
def statistics(csv_filename, bins):
    export_dir = os.path.join(app.config['UPLOAD_PATH'], 'exports/')
    image_dir = os.path.join(app.config['UPLOAD_PATH'], 'images/')

    csv_filepath = os.path.join(export_dir, csv_filename)
    if os.path.isfile(csv_filepath):
        hist_data = []

        # https://realpython.com/python-csv/
        with open(csv_filepath, mode='r') as datafile:
            data_reader = csv.reader(datafile, delimiter=',')
            line_count = 0
            for row in data_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    hist_data.append([float(row[1]), float(row[2])])
    else:
        flash('Cannot export - no CSV datafile found.')
        return redirect(url_for('index'))

    # make path to histogram explicit here.
    # https://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
    existing_files = [filename for filename in os.listdir(
        image_dir) if filename.startswith('hist')]
    for hist_filename in existing_files:
        os.remove(os.path.join(image_dir, hist_filename))

    perc_data = [i[0] for i in hist_data]
    perc_hist_filename = save_histogram(perc_data, image_dir, (0,1), bins, 'Intensity')

    area_data = [i[1] for i in hist_data]
    area_hist_filename = save_histogram(area_data, image_dir, (0,1), bins, 'Area')

    files = [csv_filename, perc_hist_filename,
             area_hist_filename]

    return render_template('statistics.html', files=files)

@app.route('/histogram/<filename>')
def histogram(filename):
    image_dir = os.path.join(app.config['UPLOAD_PATH'], 'images/')
    return send_from_directory(image_dir, filename)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/settings')
def settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    mask_dir = os.path.join(app.config['UPLOAD_PATH'], 'masks/')
    files = os.listdir(mask_dir)
    if not files:
        load_request = load_editor()
        print(load_request)

    settings = {}
    for key in config['user_settings']:
        settings[key] = config['user_settings'][key]

    return render_template('settings.html', current_settings=settings)

@app.route('/apply-settings', methods=["POST"])
def apply_settings():
    percentile = request.form['percentile']

    red_min_thresh = request.form['red_min']
    red_max_thresh = request.form['red_max']

    green_min_thresh = request.form['green_min']
    green_max_thresh = request.form['green_max']

    blue_min_thresh = request.form['blue_min']
    blue_max_thresh = request.form['blue_max']

    bins = request.form['bins']

    settings = {'pigment_percentile': percentile,
                'pigment_area_red_min': red_min_thresh,
                'pigment_area_red_max': red_max_thresh,
                'pigment_area_green_min': green_min_thresh,
                'pigment_area_green_max': green_max_thresh,
                'pigment_area_blue_min': blue_min_thresh,
                'pigment_area_blue_max': blue_max_thresh,
                'histogram_bins': bins}

    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    for key, value in settings.items():
        config.set('user_settings', key, value)

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    return redirect(url_for('settings'))

@app.route('/default-settings', methods=["POST"])
def default_settings():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'initial_threshold': '113',
                         'pigment_percentile': '15',
                         'pigment_area_red_min': '120',
                         'pigment_area_red_max':'152',
                         'pigment_area_green_min': '100',
                         'pigment_area_green_max':'140',
                         'pigment_area_blue_min': '55',
                         'pigment_area_blue_max':'120',
                         'histogram_bins':'10'}

    config['user_settings'] = {}

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    return redirect(url_for('settings'))

@app.route('/color-test', methods=["POST"])
def color_test():
    image_index = int(request.form.get('index'))
    red_min_thresh = int(request.form.get('red_min'))
    red_max_thresh = int(request.form.get('red_max'))
    green_min_thresh = int(request.form.get('green_min'))
    green_max_thresh = int(request.form.get('green_max'))
    blue_min_thresh = int(request.form.get('blue_min'))
    blue_max_thresh = int(request.form.get('blue_max'))

    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    threshold = request.cookies.get('threshold')
    thresh_array = json.loads(threshold)
    threshold = int(thresh_array[image_index - 1])

    print('Image index: ' + str(image_index))
    print('Test threshold: ' + str(threshold))

    display_dir = os.path.join(app.config['UPLOAD_PATH'], 'display/')
    files = os.listdir(display_dir)
    num_files = len(files)

    if(num_files != 0 and 0 < image_index and image_index <= num_files):
        filename = files[image_index-1]

        filepath = os.path.join(display_dir, filename)
        cimage = preprocess_image(filepath, 'c')
        preimage = preprocess_image(filepath)
        mask = threshflood(preimage, int(threshold))
        try:
            mask = remove_noise(mask)
        except IndexError:
            flash('Initial threshold is too high. Reduce to load image.')
            return redirect(url_for('settings'))
        
        area, red, green, blue, combined = quant_area(cimage, mask, 
                                                      min_otsu=[red_min_thresh, green_min_thresh, blue_min_thresh], 
                                                      max_otsu=[red_max_thresh, green_max_thresh, blue_max_thresh])
        
        color_dir = os.path.join(app.config['UPLOAD_PATH'], 'color_test/')
        if not os.path.isdir(color_dir):
            os.mkdir(color_dir)
        else:
            print('Directory exists: {}'.format(color_dir))

        existing_files = os.listdir(color_dir)
        for upload_filename in existing_files:
            os.remove(os.path.join(color_dir, upload_filename))

        save_png(cimage, 'color_original', color_dir, addtime=True)
        pigmented_pixels = numpy.where(combined == 255)
        cimage[pigmented_pixels] = [55, 255, 20]
        save_png(cimage, 'color_otsu', color_dir, addtime=True)

        plt.figure(figsize = (12,5))

        plt.subplot(1, 3, 1)
        plt.axis('off')
        plt.imshow(red)
        plt.title('Red')


        plt.subplot(1, 3, 2)
        plt.axis('off')
        plt.imshow(green)
        plt.title('Green')


        plt.subplot(1, 3, 3)
        plt.axis('off')
        plt.imshow(blue)
        plt.title('Blue')

        filename = 'color_channels' + str(time.time()) + '.png'
        filepath = os.path.join(color_dir, filename)
        plt.savefig(filepath)

        print(area)
    else:
        flash('Index error')
        abort(400)

    return jsonify(200)

@app.route('/color-image')
def color_image():
    color_dir = os.path.join(app.config['UPLOAD_PATH'], 'color_test/')
    
    color_files = os.listdir(color_dir)

    color_original = [i for i in color_files if 'color_original' in i]
    color_original_filename = os.path.basename(color_original[0])

    color_otsu = [i for i in color_files if 'color_otsu' in i]
    color_otsu_filename = os.path.basename(color_otsu[0])
    
    color_channels = [i for i in color_files if 'color_channels' in i]
    color_channels_filename = os.path.basename(color_channels[0])

    files = [color_original_filename, color_otsu_filename, color_channels_filename]

    return render_template('test_color.html', files=files)

@app.route('/cimage/<filename>')
def cimage(filename):
    image_dir = os.path.join(app.config['UPLOAD_PATH'], 'color_test/')
    return send_from_directory(image_dir, filename)
