from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("table/<str:tp>",views.render_table,name="table"),
    path("client_pdf/<str:nom_num>",views.client_pdf,name="pdf"),
    path("deposit_pdf/<str:nom_num>",views.deposit_pdf,name="dp_pdf"),
    path("fd_pdf/<str:dp_num>",views.FD_pdf,name="FD_pdf"),

    path("coll/<str:num>",views.collection_data,name="blklk"),
    path('test/', views.test),
    path("fc_coll/<str:num>",views.collection_fc,name="blklkjlk"),
    path("fc/<str:fc_num>",views.finance,name="blsssklk"),
    path("fc_pdf/<str:fc_num>",views.fc_pdf,name="bsslsssklk"),
    path("deposit_check/", views.deposit_check,name="deposit_check"),
    path("doc_check/<str:lan>", views.doc_check, name="doc_check"),
    # path("collection/", views.collection, name="collection"),
    path("transit/<str:tp>/<str:nom_num>",views.tansition,name="bsslssssklk"),
    
    #Reports Section
    path("report/<str:report_type>",views.report,name="rep"),
    # path("clientcoll_report/<str:tp>",views.ClientCollection,name="ressp"),
    # path("agentcoll_report/<str:tp>",views.AgentCollection,name="ressp"),
   
    path("cash_reciept/<str:bill_num>",views.cash_coll,name="ble"),
    path("pdf/<str:nom_num>",views.pdf,name="ble"),
    # path("ledger/",views.ledger,name="ble"),
    # path("cashbook/",views.cashbook,name="ble"),
    path("noc_pdf/<str:fc_num>",views.noc,name="ble"),
    path("id_card/<str:nom_num>",views.id_card,name="ble"),
    path("withdrawl/<str:num>",views.withdrawl,name="ble"),
    path("client/",views.client_report,name="ble"),
    path("db_select/",views.db_select,name="ble"),
    path("wd_comps/<str:acc_num>",views.wd_componets, name="s"),
    path("document/<str:nom_num>", views.document_pdf, name="document"),
    path("financecollection/<str:nom_num>", views.collectionFinance_reciept, name = 'financeCollection'),
    path("dep_collection/<str:dt>", views.deposit_collection, name='deposit_collection'),
    path("fin_collection/<str:ft>", views.finance_collection, name='finance_collection'),
    path("check_collection/", views.check_collection, name="check_collection"),
    path("print_documents/", views.print_documents, name="printdocs"),
    path("doc_data/<str:doc_type>", views.get_data_by_document),
    path("emp_data/", views.get_employees),
    path("pastcollection/<str:date>", views.past_collection),
    path("approveloan/<str:num>", views.approveloandata),
    path("accountstatus/", views.accountstatus, name="accountstatus"),
    path("changeaccountstatus/", views.changeaccountstatus, name="changeaccountstatus"),
    path("docdispatch/", views.docdispatch_tool, name="docdispatch"),
    path("dispatchdocapi/<str:lan>", views.dispatchdocapi),
    path("profitloss/", views.profitloss_report, name="profitloss"),
    path("balancesheet/", views.balance_sheet, name="balancesheet"),
    path("expenditure/", views.expenditure, name="expenditure"),
    path("uploadeddocuments/", views.uploadedDocs, name="uploadedDocs"),
    path("print_data/<str:doc>/<str:pk>", views.print_data),
    ]
    
   
    