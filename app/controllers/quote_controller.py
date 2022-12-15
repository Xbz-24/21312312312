from flask import request, redirect, render_template, Blueprint, flash, session
from app.decorators import login_required
from app.models.users import User
from app.models.quotes import Quote

quotes = Blueprint('quotes', __name__, template_folder='templates')

# rutas nuevas
@quotes.route('/quotes')
def main_quotes():
    
    
    favorites = Quote.favorites(session['user']['id'])
    quotable_quotes = Quote.quotable_quotes(session['user']['id'])
    
    #import pdb; pdb.set_trace()
    return render_template('quotes.html', quotable_quotes=quotable_quotes, favorites=favorites)


@quotes.route('/quotes/new')
def new_quote():
    return redirect('/quotes')


@quotes.route('/quotes/new', methods=['POST'])
def create_quote():
    print(f"autor:{request.form['autor']}")
    print(request.form)
    if not Quote.validate(request.form):
        return redirect('/quotes/new')
    Quote.create(
        request.form['autor'],
        request.form['mensaje'],
        session['user']['id']
    )
    return redirect('/quotes')


@quotes.route('/quotes/join/<quote_id>')
def join_quote(quote_id):
    Quote.join_quote(session['user']['id'], quote_id)
    return redirect('/quotes')


@quotes.route('/quotes/drop/<quote_id>')
def drop_quote(quote_id):
    Quote.drop_quote(session['user']['id'], quote_id)
    return redirect('/quotes')

@quotes.route('/quotes/edit/<quote_id>')  #get
def edit(quote_id):
    quote= quote_id
    return render_template("edit_quote.html",quote=quote)

@quotes.route('/quotes/edit/<quote_id>', methods=['POST']) # post=>update
def edit_quote(quote_id):
    Quote.edit_quote(
        request.form['message'],
        request.form['autor'],
        quote_id,
    )
    return redirect('/quotes')
