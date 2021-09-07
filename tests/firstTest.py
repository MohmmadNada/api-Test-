from _pytest.outcomes import Skipped, fail
import pytest
import requests
parmsObj={
        'sortBy':"price",
        'pageNum':1,
        'direction':"desc",
        'limit' : 5
    }
baseurl = 'https://fda-dev.forbes.com/tradedAssets'
@pytest.fixture
def testApiReq():
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    return bodyResponse
# test the limit by length 
def test_api_limit(testApiReq):
    assert len(testApiReq) == 5
    parmsObj['limit'] = 50
    limitTest2 = requests.get(baseurl,params=parmsObj).json()
    assert len(limitTest2['assets']) == 50
# test random name 
def test_api_name(testApiReq):
    expectedName = "Bitcoin" 
    actualName = testApiReq[0]['name']
    assert expectedName == actualName
    expectedName = "Wrapped Bitcoin"
    actualName = testApiReq[1]['name']
    assert expectedName == actualName
# test all props (attrs) from api 
def test_api_all_prop(testApiReq):
    expectedProp = ['symbol','displaySymbol','name','slug','logo','price','percentage','changeValue','marketCap','impact','volume']
    for obj in  testApiReq:
        actualKeys =list(obj.keys())
        assert actualKeys == expectedProp

def test_sortBy_price_desc(testApiReq):
    lenResp =len(testApiReq)
    for objectResp in range(lenResp-1):
        assert ( testApiReq[objectResp]['price'] > testApiReq[objectResp+1]['price'] ) 

#  test sort by price case asc and desc 
def test_sortBy_price_asc():
    parmsObj['direction'] = 'asc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    lenResp =len(bodyResponse)
    for objectResp in range(lenResp-1):
        assert( bodyResponse[objectResp]['price'] < bodyResponse[objectResp+1]['price'] ) 
# ......................................... sort by name test section  ............. 
def test_sortBy_name():
    parmsObj['sortBy']='name'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    allNamesApi = []
    for objApi in bodyResponse:
        allNamesApi.append(objApi['name'])
    actualNames = allNamesApi
    expectedNames = list(allNamesApi)
    sorted(expectedNames)
    for i in range(len(expectedNames)) :  
        assert(actualNames[i]==expectedNames[i])
# ......................................... 1. sort by impact test section asc  ............. 
def test_sortImpact_asc():
    parmsObj['sortBy']='impact'
    parmsObj['direction']='asc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    responseAssets = bodyResponse
    notSortImpacts=[]
    for objResp in responseAssets :
        notSortImpacts.append(objResp['impact'])
    SortImpacts = sorted(notSortImpacts)
    assert SortImpacts == notSortImpacts 
# ......................................... 2. sort by impact test section desc ............. 
def test_sortImpact_desc():
    parmsObj['sortBy']='impact'
    parmsObj['direction']='desc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    responseAssets = bodyResponse
    notSortImpacts=[]
    for objResp in responseAssets :
        notSortImpacts.append(objResp['impact'])
    SortImpacts = sorted(notSortImpacts,reverse=True)
    assert SortImpacts == notSortImpacts 

# ......................................... 1. sort by change, desc ............. Fail ************** somthing wrong 
# ......................................... 1. sort by change, asc ............. 
def test_sortBy_change():
    parmsObj['sortBy']='change' # should sort by percentage index 0 is higher   
    parmsObj['direction']='desc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    actualChanges = []
    for objResp in bodyResponse :
        actualChanges.append(objResp['percentage'])
    expectedChanges = sorted(actualChanges,reverse=True)
    for i in range(len(expectedChanges)):
        assert expectedChanges[i] == actualChanges[i]
# ***********   *********** test sort by marketCap , 1. desc 2. sec *********** ***********
def test_sortBy_marketCap_01():
    parmsObj['sortBy']='marketCap'
    parmsObj['direction']='desc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    actualValues = [] 
    for objResp in bodyResponse: 
        actualValues.append(objResp['marketCap'])
    axpectedValues = sorted(actualValues,reverse=True)
    assert actualValues == axpectedValues
def test_sortBy_marketCap_02():
    parmsObj['sortBy']='marketCap'
    parmsObj['direction']='asc'
    req = requests.get(baseurl,params=parmsObj).json()
    bodyResponse = req['assets']
    actualValues = [] 
    for objResp in bodyResponse: 
        actualValues.append(objResp['marketCap'])
    axpectedValues = sorted(actualValues)
    assert actualValues == axpectedValues    