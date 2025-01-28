# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_invoices.py

DESCRIPTION:
    This sample demonstrates how to analyze invoices.

    See fields found on a invoice here:
    https://aka.ms/azsdk/formrecognizer/invoicefieldschema

USAGE:
    python sample_analyze_invoices.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
"""

import os
from dotenv import load_dotenv

#Load environment and check variables
load_dotenv('/Users/toniletempt/Projects/UPSKILLING-Q3-25/.env')

def analyze_invoice():
    path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "/Users/toniletempt/Projects/upskilling-q3-25/sample_forms/orders/pdfs/EchelonCycleOrder.pdf"
        )
    )

    # [START analyze_invoices]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature, AnalyzeResult

    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice", body=f,
            features=[DocumentAnalysisFeature.QUERY_FIELDS],
            query_fields=["Savings", "discount","Subtotal","Tax","Total"],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    print("Here are extra fields in result:\n")
    if result.documents:
        for doc in result.documents:
            if doc.fields and doc.fields["Subtotal"]:
                print(f"Subtotal: {doc.fields['Subtotal'].value_string}")
            if doc.fields and doc.fields["Savings"]:
                print(f"Savings: {doc.fields['Savings'].value_string}")
            if doc.fields and doc.fields["discount"]:
                print(f"Associate Discount: {doc.fields['discount'].value_string}")
            if doc.fields and doc.fields["Tax"]:
                print(f"Tax: {doc.fields['Tax'].value_string}")
            if doc.fields and doc.fields["Total"]:
                print(f"Total: {doc.fields['Total'].value_string}")

    # [END analyze_query_fields]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError

    try:
        analyze_invoice()
    except HttpResponseError as error:
        print(
            "For more information about troubleshooting errors, see the following guide: "
            "https://aka.ms/azsdk/python/formrecognizer/troubleshooting"
        )
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise