from django.shortcuts import render, HttpResponse
from .models import (Account, PublicationData, Attributes,
                SalesTerm, Pictures, Description, OrigintoCopy)
from django.contrib.auth.decorators import login_required


import logging
import requests
import json

from .forms import CopyForm, UpdateForm

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


###########################     Seccion de Update      #####################
@login_required
def update(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            message, updated_pubs = update_continue(request)
            len_pubs_update = len(updated_pubs)
            return render(request, 'template.html', 
            {'form': form, 
            'message': message,
            'len_pubs_update': len_pubs_update,
            'updated_pubs': updated_pubs})
    else:
        form = UpdateForm()
    return render(request, 'template.html', {'form': form})


def update_continue(request):
    name = request.POST.get('account')
    account = Account.objects.get(name=name)
    PublicationData.objects.filter(account=account).delete()
    _user_id = account.user_id
    _access_token = account.access_token
    url = 'https://api.mercadolibre.com/users/{}/items/search?access_token={}&status=active'.format(_user_id, _access_token)

    response = requests.get(url)
    if not response.status_code == requests.codes.ok:
        message = "request no valido. status code = {} - \
            revisar credenciales de la cuenta".format(response.status_code)
        logger.warn(message)
        return message

    iteractions = (int(response.json()['paging']['total']) // 50) + 1
    init = (account.offset_query // 50)
    range_iteractions = range(init, iteractions)
    for i in range_iteractions:
        offset = i * 50
        account.offset_query = offset
        account.save()
        url = 'https://api.mercadolibre.com/users/{}/items/search?access_token={}&status=active&offset={}'.format(_user_id, _access_token, offset)
        logger.info(url)
        response = requests.get(url)
        r = response.json()
        items = r.get('results', None)    
        if not items:
            message = "Esta cuenta no posee publicaciones activas"
            logger.warn(message)
            return message

        #get item data
        updated_pubs = []
        for item in items:
            url = 'https://api.mercadolibre.com/items/{0}'.format(item)
            re = requests.get(url)
            if not re.status_code == requests.codes.ok:
                continue
            data = re.json()

            ObjPub = get_or_create_publication(data, account)
            set_or_create_image(ObjPub, data)
            set_or_create_description(ObjPub, data, item)
            set_or_create_sales_terms(ObjPub, data)
            set_or_create_attributes(ObjPub, data)
            updated_pubs.append(ObjPub.title)
            
        message = "Cuentas con publicaciones actualizadas, por favor verificar en el admin."
        logger.warn(message)
        if offset == 1000:
            break
    return message, updated_pubs


def get_or_create_publication(data, account):
    meli_id = data['id']
    title = data['title'] 
    category_id = data['category_id']
    price = data['price']
    currency_id = data['currency_id']
    available_quantity = data['available_quantity']
    buying_mode = data['buying_mode']
    listing_type_id = data['listing_type_id']
    video_id = data['video_id']
    try:
        pub = PublicationData.objects.get(meli_id=meli_id)
    except:
        pub = PublicationData(
            account=account,
            meli_id=meli_id,
        )
    pub.title=title
    pub.category_id=category_id
    pub.price=price
    pub.currency_id=currency_id
    pub.available_quantity=available_quantity
    pub.buying_mode=buying_mode
    pub.listing_type_id=listing_type_id
    pub.video_id=video_id        
            
    pub.save()
    return pub


def set_or_create_image(ObjPub, data):
    pictures = data['pictures']
    for img in pictures:
        url = img['url']
        try:
            ObjPic = Pictures.objects.get(publication_data=ObjPub, source=url)
        except:
            ObjPic = Pictures(publication_data=ObjPub, source=url)
        ObjPic.save()


def set_or_create_description(ObjPub, data, item):
    url = "https://api.mercadolibre.com/items/{0}/description".format(item)
    r = requests.get(url)
    if not r.status_code == requests.codes.ok:
        return
    description = r.json()['plain_text']
    try:
        ObjDesc = Description.objects.get(publication_data=ObjPub)
    except:
        ObjDesc = Description(publication_data=ObjPub)
    ObjDesc.description=description
    ObjDesc.save()


def set_or_create_sales_terms(ObjPub, data):
    terms = data['sale_terms']
    for term in terms:
        sale_terms=term['value_name']
        id_sale_terms=term['id']
        value_id_terms=term['value_id']
        try:
            ObjTerm = SalesTerm.objects.get(publication_data=ObjPub, \
                sale_terms=sale_terms, id_sale_terms=id_sale_terms, \
                value_id_terms = value_id_terms)
        except:
            ObjTerm = SalesTerm(publication_data=ObjPub, \
                sale_terms=sale_terms, id_sale_terms=id_sale_terms, \
                value_id_terms = value_id_terms)
        ObjTerm.save()


def set_or_create_attributes(ObjPub, data):
    attributes = data['attributes']
    for attribute in attributes:
        ObjAttr = None
        id_attributes=attribute['id']
        value_attributes=attribute['value_id']
        try:
            ObjAttr = Attributes.objects.get(publication_data=ObjPub, \
                id_attributes=id_attributes, value_attributes=value_attributes)
        except:
            ObjAttr = Attributes(publication_data=ObjPub, \
                id_attributes=id_attributes, value_attributes=value_attributes)
        if not ObjAttr is None:
            ObjAttr.save()
######################################################################################


###########################     Seccion de Create      #################################
'''
{
    "title":"Item de test - No Ofertar",
    "category_id":"MLA3530",
    "price":10,
    "currency_id":"ARS",
    "available_quantity":1,
    "buying_mode":"buy_it_now",
    "listing_type_id":"gold_special",
    "description": "Item de test - No Ofertar",
    "video_id": "YOUTUBE_ID_HERE",
    “attributes”: [
        { "id" : "ITEM_CONDITION", "value_id": "2230582"} 
    ]
    "sale_terms":[
        {“id”: “WARRANTY_TYPE”, “value_id”: 2230279 },
        {“id”: “WARRANTY_TIME”, “value_name”: “90 dias”}
    ]
    "pictures":[
        {"source":"http://mla-s2-p.mlstatic.com/968521-MLA20805195516_072016-O.jpg"}
    ]
}'

'''
@login_required
def create(request):
    if request.method == 'POST':
        form = CopyForm(request.POST)
        if form.is_valid():
            message, pubs_no_copy, pubs_copy = copy(request)
            len_pubs_no_copy = len(pubs_no_copy)
            len_pubs_copy = len(pubs_copy)
            return render(request, 'template.html',
            {'form': form, 
            'message': message, 
            'pubs_no_copy': pubs_no_copy,
            'len_pubs_no_copy': len_pubs_no_copy,
            'len_pubs_copy': len_pubs_copy,
            'pubs_copy': pubs_copy})
    else:
        form = CopyForm()
    return render(request, 'template.html', {'form': form})

def copy(request):
    message = 'No se selecciono alguna publicacion para copiar'
    pubs_no_copy = []
    pubs_copy = []    
    name_from_copy = request.POST.get('from_account')
    name_to_copy = request.POST.get('to_account')

    account_original = Account.objects.get(name=name_from_copy)
    account_origin_id = account_original.user_id
  
    account_copy = Account.objects.get(name=name_to_copy) 
    account_copy_id = account_copy.user_id
    access_token = account_copy.access_token
    
    # publicaciones a copiar cuenta Origin
    Pubs = PublicationData.objects.filter(account=account_original)
    
    for Pub in Pubs:
        # Verifica si se tildo para copiar
        if not Pub.copy:
            continue
        pub_origin_id = Pub.meli_id
        try:
            get_pub = OrigintoCopy.objects.get(
                account_origin=account_origin_id,
                account_copy=account_copy_id,
                pub_id_origin=pub_origin_id                
            )
            message = 'Ya fue copia este objeto. Con el ID={} este fue copiado de la \
            cuenta:{} a la cuenta:{}'.format(get_pub.pub_id_Copy, account_original.name, account_copy.name)
            logger.info(message)
            continue
        except:            
            _description = Description.objects.filter(publication_data=Pub)[0]
            if _description:
                description = {'plain_text': _description.description}
        
            _Pictures = Pictures.objects.filter(publication_data=Pub)
            pictures = []
            for Pic in _Pictures:
                pictures.append({
                    'source': Pic.source
                })
        
            _Sale_Terms = SalesTerm.objects.filter(publication_data=Pub)
            
            terms = []
            for Term in _Sale_Terms:
                _dict = {
                    'id':Term.id_sale_terms,
                    'value_name':Term.sale_terms,
                }
                if Term.value_id_terms:
                    _dict['value_id'] = str(Term.value_id_terms)
                terms.append(_dict)

            _Attributes = Attributes.objects.filter(publication_data=Pub)
            attributes = []
            for attr in _Attributes:
                attributes.append({
                    'id':attr.id_attributes,
                    'value_id':attr.value_attributes
                })

            data = {
                'title':Pub.title,
                'category_id':Pub.category_id,
                'price':float(Pub.price),
                'currency_id':Pub.currency_id,
                'available_quantity':int(Pub.available_quantity),
                'buying_mode':Pub.buying_mode,
                'listing_type_id':Pub.listing_type_id,
                'description':description,
                'video_id':Pub.video_id,
                'attributes': attributes,
                'sale_terms':terms,
                'pictures': pictures
            }

            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            url = 'https://api.mercadolibre.com/items?access_token={0}'.format(access_token)
            body = json.dumps(data)
            response = requests.post(url, body, headers=headers)
            if response.status_code >= 300:
                message = "request no valido. status code = {0} - \
                Publicacion title: {1}".format(response.status_code, Pub.title)
                logger.warn(message)
                pubs_no_copy.append(Pub.title)
                continue
            pubs_copy.append(Pub.title)
            pub_copy_id=response.json()['id']
            logger.info('Objeto creado en MeLi con ID:{}'.format(pub_copy_id))
            import pdb; pdb.set_trace()
            OrigintoCopy(
                account_origin=account_origin_id,
                account_copy=account_copy_id,
                pub_id_origin=pub_origin_id,
                pub_id_Copy=pub_copy_id).save()
        message = 'Proceso terminado'
        logger.info(message)
    
    return message, pubs_no_copy, pubs_copy
