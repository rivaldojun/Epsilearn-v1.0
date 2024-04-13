from flask import render_template,jsonify,redirect,url_for,request,session
from sqlalchemy import and_
from App.Models.models import *
from App.Controllers.fonction import *
import stripe
import os
from App.Main.routes_about import MainBp

# @MainBp.after_request
# def add_no_cache_headers(response):
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     return response


@MainBp.route('/cancel')
def checkout_cancel():
    return render_template('cancel.html')

#PAYEMENT MANAGEMENT
@MainBp.route('/checkout/<amount>/<langue>')
def checkout(amount,langue):
    amount = int(amount)*100
    
    return render_template('checkout.html',key=os.getenv("STRIPE_PUBLIC_KEY"),amount=amount,langue=langue)

@MainBp.route('/create-checkout-session-langue/<langue>/<amount>', methods=['POST'])
def create_checkout_session_langue(langue,amount):
    try:
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name':"Abonnement de"+langue,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=os.getenv("YOUR_DOMAIN") + '/charge/'+amount+'/'+langue,
            cancel_url=os.getenv("YOUR_DOMAIN") + '/cancel',
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@MainBp.route('/charge/<prix>/<langue>',methods=["POST","GET"])
def charge(prix,langue): 
    amount = int(prix)
    # Amount in cents
    if amount==800:
        duree=1
    elif amount==2000:
        duree=3
    else :
        duree=6
    amount = int(amount)/100
    user_id = session.get('userid')
    ab=AbonnementLangue.query.filter(and_(AbonnementLangue.id_abonne==user_id,AbonnementLangue.nom==langue)).first()
    if ab:
        ab.termine="non"
        ab.duree=duree
        ab.nb=ab.nb+1
        datedebut = datetime.now().date()
        ab.datedebut=datedebut
        ab.datefin=datedebut + timedelta(days=duree * 30)
        db.session.add(ab)
        db.session.commit()
    else:
        abonnement=AbonnementLangue(id_abonne=user_id,datedebut = datetime.now().date(), datefin = datetime.now().date() + timedelta(days=duree * 30),termine="non",duree=duree,nom=session.get("langue"),point=session.get("point"))
        db.session.add(abonnement)
        db.session.commit()
    return render_template('charge.html', amount=amount)

@MainBp.route('/payementdemande/<id_demande>',methods=["POST","GET"])
def payementdemande(id_demande):
    
    demande = Demande.query.get(id_demande)
    amount=demande.prix
    demande.statut_payement="payer"
    db.session.commit()
    amount = int(amount)
    return render_template('charge.html', amount=amount)

@MainBp.route('/checkoutdemande/<id_demande>')
def checkoutdemande(id_demande):
    
    demande = Demande.query.get(id_demande)
    amount=demande.prix
    amount = int(amount)*100
    return render_template('checkoutdemande.html',key=os.getenv("STRIPE_PUBLIC_KEY"),amount=amount,id_demande=id_demande)

@MainBp.route('/create-checkout-session-demande/<id>', methods=['POST'])
def create_checkout_session_demande(id):
    try:
        
        demande = Demande.query.get(id)
        amount=demande.prix
        amount = int(amount)*100
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name':demande.chapiter,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payementdemande/'+id,
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@MainBp.route('/payementoffre/<id_offre>',methods=["POST","GET"])
def payementoffre(id_offre):
    offre = Offre.query.get(id_offre)
    amount=offre.prix
    part=SubscriptionOffre(id_offre=id_offre,id_participant=user.id)
    db.session.add(part)
    db.session.commit()
    amount = float(amount)
    return render_template('charge.html', amount=amount)

@MainBp.route('/checkoutoffre/<id_offre>')
def checkoutoffre(id_offre):
    offre = Offre.query.get(id_offre)
    amount=offre.prix
    amount = int(amount)*100
    return render_template('checkoutoffre.html',key=os.getenv("STRIPE_PUBLIC_KEY"),amount=amount,id_offre=id_offre)

@MainBp.route('/create-checkout-session-offre/<id>', methods=['POST'])
def create_checkout_session_offre(id):
    try:  
        offre = Offre.query.get(id)
        amount=offre.prix
        amount = int(amount)*100
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name':offre.nom_offre,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=os.getenv("YOUR_DOMAIN") + '/payementoffre/'+id,
            cancel_url=os.getenv("YOUR_DOMAIN") + '/cancel',
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)
#END PAYEMENT MANAGEMENT

