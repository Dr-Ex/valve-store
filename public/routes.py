from flask import g
from flask import render_template
from flask import request
from flask import redirect
import flask_login
from public import website
from public import datamanager

@website.route('/')
def index():
	query_string = ('SELECT * FROM valves')
	
	query_results = datamanager.query_db(
		query_string, 
		[], 
		one=False
	)

	return render_template('index.html', items=query_results)

@website.route('/item/<model_no>', methods=['GET', 'POST'])
def item(model_no = None):

	if request.method == 'GET':
		query_string = (
			'SELECT * from valves '
			'WHERE model_no = ?'
		)

		query_results = datamanager.query_db(
			query_string,
			[model_no],
			one=True
		)

		return render_template('item.html', item=query_results)

	if request.method == 'POST':
		model_no = request.form.get('model_no')
		product_qty = request.form.get('product_qty')

		return redirect('/checkout/{}'.format(model_no))

@website.route('/checkout/<model_no>', methods=['GET', 'POST'])
def checkout(model_no = None):
	if request.method == 'GET':
		query_string = (
			'SELECT * from valves '
			'WHERE model_no = ?'
		)

		query_results = datamanager.query_db(
			query_string,
			[model_no],
			one=True
		)

		return render_template('checkout.html', item=query_results)

	if request.method == 'POST':
		name = request.form.get('name')
		address = "{}, {} {}, {}".format(
			request.form.get('street'), request.form.get('city'), 
			request.form.get('postcode'), request.form.get('country'))
		purchase_qty = request.form.get('purchase_qty')
		item_id = request.form.get('item_id')
		card_number = request.form.get('card_number')
		card_name = request.form.get('card_name')
		card_expiry = request.form.get('card_expiry')
		card_security = request.form.get('card_security')

		# if len(card_number) not 16:
		# 	return redirect('/checkout/', model_no = item_id)

		query_string = (
			'INSERT INTO orders (name, address, item_id, purchase_qty, '
			'card_number, card_name, card_expiry, card_security) '
			'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
		)

		query_results = datamanager.query_db(
			query_string,
			[name, address, item_id, purchase_qty, card_number, card_name, card_expiry, card_security],
			one=False
		)

		return redirect('/thank-you')

@website.route('/thank-you')
def thank_you():
	# latest_id = datamanager.query_db('SELECT MAX(ID) FROM orders', [], one=True)
	
	# query_string = (
	# 	'SELECT name, item_id, purchase_qty '
	# 	'FROM orders WHERE ID = ?'
	# )
	# order_info = datamanager.query_db(
	# 	query_string,
	# 	[latest_id],
	# 	one=False
	# )


	# product_info = datamanager.query_db(
	# 	'SELECT model_no FROM valves WHERE ID = ?',
	# 	[],
	# 	one=True
	# )


	return render_template('thank-you.html')

