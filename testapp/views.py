# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import StockData
from .models import Document
from dateutil import parser as date_parser
from .forms import UploadFileForm
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import F
import pprint
import datetime, xlrd
import MySQLdb
import json

test = 'c'

db = MySQLdb.connect(host="localhost", 
                     user="root", 
                     passwd="mavrick786", 
                     db="riskdb")

def index(request):
  form = UploadFileForm() # A empty, unbound form

 

  # Render list page with the documents and the form
  # return render_to_response(
  #   'index.html',
  #   {'stockDatas': stockDatas, 'form': form, 'test': test},
  #   RequestContext(request)
  # )
  return render_to_response(
    'index.html',
    {'form': form},
    RequestContext(request)
  )


@csrf_exempt
def getData(request):
  postData = request.POST
  itemsPerPage = postData.get('itemsPerPage')
  page = postData.get('page')
  filters = postData.get('filters')
  sort = postData.get('sort')
  sortreverse = postData.get('sortreverse')

  page = int(page)
  itemsPerPage = int(itemsPerPage)

  if "null" in filters:
    stockDatas = StockData.objects.all()
  else:
    start_date = postData.get('dateFrom')
    start_date = date_parser.parse(start_date)
    end_date = postData.get('dateTo')
    end_date = date_parser.parse(end_date)
    if 'none' not in filters:
      if "loss"  in filters:
        stockDatas = StockData.objects.filter(date__range=(start_date, end_date), open__gt=F('close'))
      else:
        stockDatas = StockData.objects.filter(date__range=(start_date, end_date), close__gt=F('open'))
    else:
      stockDatas = StockData.objects.filter(date__range=(start_date, end_date))


  if sortreverse == "true":
    stockDatas = stockDatas.order_by("-" + sort)
  else:
    stockDatas = stockDatas.order_by(sort)


  totalCount = stockDatas.count()
  
  paginator = Paginator(stockDatas, itemsPerPage)
  try:
    stockDatas = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    stockDatas = paginator.page(1)

  response_data = serializers.serialize('json', stockDatas)
  return JsonResponse({"data": response_data, "count" : totalCount}, safe=False)


# Create your views here.
@csrf_exempt
def upload(request):
  if request.method == "POST":
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      newdoc = Document(docfile = request.FILES['docfile'])
      newdoc.save()
      newdoc = newdoc.docfile.name
      newdoc = str(newdoc)
      wb = xlrd.open_workbook(newdoc)
      sheet = wb.sheet_by_index(0)
      c = 1


      # Create the INSERT INTO sql query
      query = """INSERT INTO testapp_stockdata(date, open, high, low, close, volume, adj_close, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

      cursor = db.cursor()

      for r in range(1, sheet.nrows):
        r_date = sheet.cell(r, 0).value
        r_date = datetime.datetime(*xlrd.xldate_as_tuple(r_date, wb.datemode))
        r_open = sheet.cell(r, 1).value
        r_high = sheet.cell(r, 2).value
        r_low = sheet.cell(r, 3).value
        r_close = sheet.cell(r, 4).value
        r_volume = sheet.cell(r, 5).value
        r_adj_close = sheet.cell(r, 6).value
        r_stock = sheet.cell(r, 7).value
        
        # Assign values from each row
        values = (r_date, r_open, r_high, r_low, r_close, r_volume, r_adj_close, r_stock)
        # Execute sql Query
        cursor.execute(query, values)

        c=c+1

      # Close the cursor
      cursor.close()

      # Commit the transaction
      db.commit()

      # Close the database connection
      db.close()
      return render_to_response('index.html', {'fileupload' : "true"}, RequestContext(request))
    else:
      return render_to_response(
        'index.html',
        {'form': form},
        RequestContext(request)
      )
  else:
    return render_to_response(
      'index.html',
      {},
      RequestContext(request)
    )
