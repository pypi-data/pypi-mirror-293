

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = (n % 1 == 0 && n % 10 == 1 && n % 100 != 11 ? 0 : n % 1 == 0 && n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? 1 : n % 1 == 0 && (n % 10 ==0 || (n % 10 >=5 && n % 10 <=9) || (n % 100 >=11 && n % 100 <=14 )) ? 2: 3);
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "=": "=",
    "Add condition": "\u0414\u043e\u0434\u0430\u0439\u0442\u0435 \u0443\u043c\u043e\u0432\u0443",
    "Additional information required": "\u041d\u0435\u043e\u0431\u0445\u0456\u0434\u043d\u0430 \u0434\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f",
    "All": "\u0412\u0441\u0435",
    "All of the conditions below (AND)": "\u0423\u0441\u0456 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0456 \u043d\u0438\u0436\u0447\u0435 \u0443\u043c\u043e\u0432\u0438 (\u0406)",
    "An error has occurred.": "\u0421\u0442\u0430\u043b\u0430\u0441\u044f \u043f\u043e\u043c\u0438\u043b\u043a\u0430.",
    "An error of type {code} occurred.": "\u0412\u0438\u043d\u0438\u043a\u043b\u0430 \u043f\u043e\u043c\u0438\u043b\u043a\u0430 \u0442\u0438\u043f\u0443 {code}.",
    "Apple Pay": "Apple Pay",
    "April": "\u043a\u0432\u0456\u0442\u0435\u043d\u044c",
    "At least one of the conditions below (OR)": "\u041f\u0440\u0438\u043d\u0430\u0439\u043c\u043d\u0456 \u043e\u0434\u043d\u0430 \u0437 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0445 \u043d\u0438\u0436\u0447\u0435 \u0443\u043c\u043e\u0432 (\u0410\u0411\u041e)",
    "August": "\u0441\u0435\u0440\u043f\u0435\u043d\u044c",
    "BLIK": "BLIK",
    "Bancontact": "Bancontact",
    "Barcode area": "\u041e\u0431\u043b\u0430\u0441\u0442\u044c \u0448\u0442\u0440\u0438\u0445-\u043a\u043e\u0434\u0443",
    "Boleto": "Boleto",
    "Calculating default price\u2026": "\u0420\u043e\u0437\u0440\u0430\u0445\u0443\u043d\u043e\u043a \u0446\u0456\u043d\u0438 \u0437\u0430 \u0437\u0430\u043c\u043e\u0432\u0447\u0443\u0432\u0430\u043d\u043d\u044f\u043c\u2026",
    "Cancel": "\u0421\u043a\u0430\u0441\u0443\u0432\u0430\u0442\u0438",
    "Canceled": "\u0421\u043a\u0430\u0441\u043e\u0432\u0430\u043d\u043e",
    "Cart expired": "\u0422\u0435\u0440\u043c\u0456\u043d \u0434\u0456\u0457 \u043a\u043e\u0448\u0438\u043a\u0430 \u0437\u0430\u043a\u0456\u043d\u0447\u0438\u0432\u0441\u044f",
    "Check-in QR": "\u0420\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u044f \u0437 QR",
    "Checked-in Tickets": "\u0417\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u043e\u0432\u0430\u043d\u0456 \u043a\u0432\u0438\u0442\u043a\u0438",
    "Click to close": "\u041d\u0430\u0442\u0438\u0441\u043d\u0456\u0442\u044c, \u0449\u043e\u0431 \u0437\u0430\u043a\u0440\u0438\u0442\u0438",
    "Close message": "\u0417\u0430\u043a\u0440\u0438\u0442\u0438 \u043f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u043d\u044f",
    "Comment:": "\u041a\u043e\u043c\u0435\u043d\u0442\u0430\u0440:",
    "Confirming your payment \u2026": "\u041f\u0456\u0434\u0442\u0432\u0435\u0440\u0434\u0436\u0443\u0454\u0442\u044c\u0441\u044f \u0432\u0430\u0448 \u043f\u043b\u0430\u0442\u0456\u0436\u2026",
    "Contacting Stripe \u2026": "\u0417'\u0454\u0434\u043d\u0443\u0454\u043c\u043e\u0441\u044f \u0437\u0456 Stripe\u2026",
    "Contacting your bank \u2026": "\u0417'\u0454\u0434\u043d\u0443\u0454\u043c\u043e\u0441\u044f \u0437 \u0412\u0430\u0448\u0438\u043c \u0431\u0430\u043d\u043a\u043e\u043c \u2026",
    "Continue": "\u041f\u0440\u043e\u0434\u043e\u0432\u0436\u0438\u0442\u0438",
    "Copied!": "\u0421\u043a\u043e\u043f\u0456\u0439\u043e\u0432\u0430\u043d\u043e!",
    "Count": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c",
    "Credit Card": "\u041a\u0440\u0435\u0434\u0438\u0442\u043d\u0430 \u043a\u0430\u0440\u0442\u043a\u0430",
    "Current date and time": "\u041f\u043e\u0442\u043e\u0447\u043d\u0430 \u0434\u0430\u0442\u0430 \u0442\u0430 \u0447\u0430\u0441",
    "Current day of the week (1 = Monday, 7 = Sunday)": "\u041f\u043e\u0442\u043e\u0447\u043d\u0438\u0439 \u0434\u0435\u043d\u044c \u0442\u0438\u0436\u043d\u044f (1 = \u043f\u043e\u043d\u0435\u0434\u0456\u043b\u043e\u043a, 7 = \u043d\u0435\u0434\u0456\u043b\u044f)",
    "Current entry status": "\u041f\u043e\u0442\u043e\u0447\u043d\u0438\u0439 \u0441\u0442\u0430\u043d \u0437\u0430\u043f\u0438\u0441\u0443",
    "Currently inside": "\u041d\u0430 \u0434\u0430\u043d\u0438\u0439 \u043c\u043e\u043c\u0435\u043d\u0442 \u0432\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0456",
    "December": "\u0433\u0440\u0443\u0434\u0435\u043d\u044c",
    "Do you really want to leave the editor without saving your changes?": "\u0412\u0438 \u0434\u0456\u0439\u0441\u043d\u043e \u0445\u043e\u0447\u0435\u0442\u0435 \u0432\u0438\u0439\u0442\u0438 \u0437 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0430, \u043d\u0435 \u0437\u0431\u0435\u0440\u0456\u0433\u0430\u044e\u0447\u0438 \u0437\u043c\u0456\u043d\u0438?",
    "Duplicate": "\u0414\u0443\u0431\u043b\u044e\u0432\u0430\u0442\u0438",
    "Enter page number between 1 and %(max)s.": "\u0412\u043a\u0430\u0436\u0456\u0442\u044c \u043d\u043e\u043c\u0435\u0440 \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0438 \u043c\u0456\u0436 1 \u0442\u0430 %(max)s.",
    "Entry": "\u0412\u0445\u0456\u0434",
    "Entry not allowed": "\u0412\u0445\u0456\u0434 \u0437\u0430\u0431\u043e\u0440\u043e\u043d\u0435\u043d\u043e",
    "Error while uploading your PDF file, please try again.": "\u041f\u0456\u0434 \u0447\u0430\u0441 \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f PDF-\u0444\u0430\u0439\u043b\u0443 \u0441\u0442\u0430\u043b\u0430\u0441\u044f \u043f\u043e\u043c\u0438\u043b\u043a\u0430. \u041f\u043e\u0432\u0442\u043e\u0440\u0456\u0442\u044c \u0441\u043f\u0440\u043e\u0431\u0443.",
    "Event admission": "\u0412\u0445\u0456\u0434 \u0434\u043e \u043f\u043e\u0434\u0456\u0457",
    "Event end": "\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u044f \u043f\u043e\u0434\u0456\u0457",
    "Event start": "\u041f\u043e\u0447\u0430\u0442\u043e\u043a \u043f\u043e\u0434\u0456\u0457",
    "Exit": "\u0412\u0438\u0445\u0456\u0434",
    "Exit recorded": "\u0412\u0438\u0445\u0456\u0434 \u0437\u0430\u043f\u0438\u0441\u0430\u043d\u043e",
    "February": "\u043b\u044e\u0442\u0438\u0439",
    "Fr": "\u041f\u0442",
    "Generating messages \u2026": "\u0421\u0442\u0432\u043e\u0440\u044e\u044e\u0442\u044c\u0441\u044f \u043f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u043d\u044f\u2026",
    "Google Pay": "Google Pay",
    "Group of objects": "\u0413\u0440\u0443\u043f\u0430 \u043e\u0431'\u0454\u043a\u0442\u0456\u0432",
    "Image area": "\u041e\u0431\u043b\u0430\u0441\u0442\u044c \u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f",
    "Information required": "\u041d\u0435\u043e\u0431\u0445\u0456\u0434\u043d\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f",
    "Invalid page number.": "\u041d\u0435\u0434\u0456\u0439\u0441\u043d\u0438\u0439 \u043d\u043e\u043c\u0435\u0440 \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0438.",
    "Ita\u00fa": "Ita\u00fa",
    "January": "\u0441\u0456\u0447\u0435\u043d\u044c",
    "July": "\u043b\u0438\u043f\u0435\u043d\u044c",
    "June": "\u0447\u0435\u0440\u0432\u0435\u043d\u044c",
    "Load more": "\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438 \u0431\u0456\u043b\u044c\u0448\u0435",
    "March": "\u0431\u0435\u0440\u0435\u0437\u0435\u043d\u044c",
    "Marked as paid": "\u041f\u043e\u0437\u043d\u0430\u0447\u0435\u043d\u043e \u044f\u043a \u043e\u043f\u043b\u0430\u0447\u0435\u043d\u0435",
    "Maxima": "Maxima",
    "May": "\u0442\u0440\u0430\u0432\u0435\u043d\u044c",
    "Mercado Pago": "Mercado Pago",
    "Minutes since first entry (-1 on first entry)": "\u0425\u0432\u0438\u043b\u0438\u043d \u0437 \u043f\u0435\u0440\u0448\u043e\u0433\u043e \u0432\u0445\u043e\u0434\u0443 (-1 \u043f\u0440\u0438 \u043f\u0435\u0440\u0448\u043e\u043c\u0443 \u0432\u0445\u043e\u0434\u0456)",
    "Minutes since last entry (-1 on first entry)": "\u0425\u0432\u0438\u043b\u0438\u043d \u0437 \u043e\u0441\u0442\u0430\u043d\u043d\u044c\u043e\u0433\u043e \u0432\u0445\u043e\u0434\u0443 (-1 \u043f\u0440\u0438 \u043f\u0435\u0440\u0448\u043e\u043c\u0443 \u0432\u0445\u043e\u0434\u0456)",
    "Mo": "\u041f\u043d",
    "MyBank": "MyBank",
    "No": "\u041d\u0456",
    "No active check-in lists found.": "\u0410\u043a\u0442\u0438\u0432\u043d\u0438\u0445 \u0441\u043f\u0438\u0441\u043a\u0456\u0432 \u0440\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u0457 \u043d\u0435 \u0437\u043d\u0430\u0439\u0434\u0435\u043d\u043e.",
    "No tickets found": "\u041a\u0432\u0438\u0442\u043a\u0456\u0432 \u043d\u0435 \u0437\u043d\u0430\u0439\u0434\u0435\u043d\u043e",
    "None": "\u0416\u043e\u0434\u043d\u043e\u0433\u043e",
    "November": "\u043b\u0438\u0441\u0442\u043e\u043f\u0430\u0434",
    "Number of days with a previous entry": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0434\u043d\u0456\u0432 \u0456\u0437 \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u043c \u0432\u0445\u043e\u0434\u043e\u043c",
    "Number of days with a previous entry before": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0434\u043d\u0456\u0432 \u0456\u0437 \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u043c \u0432\u0445\u043e\u0434\u043e\u043c \u0434\u043e",
    "Number of days with a previous entry since": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0434\u043d\u0456\u0432 \u0456\u0437 \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u043c \u0432\u0445\u043e\u0434\u043e\u043c \u0437",
    "Number of previous entries": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0445 \u0432\u0445\u043e\u0434\u0456\u0432",
    "Number of previous entries before": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0445 \u0432\u0445\u043e\u0434\u0456\u0432 \u0434\u043e",
    "Number of previous entries since": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0445 \u0432\u0445\u043e\u0434\u0456\u0432 \u0437",
    "Number of previous entries since midnight": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0445 \u0432\u0445\u043e\u0434\u0456\u0432 \u0437 \u043e\u043f\u0456\u0432\u043d\u043e\u0447\u0456",
    "OXXO": "OXXO",
    "Object": "\u041e\u0431'\u0454\u043a\u0442",
    "October": "\u0436\u043e\u0432\u0442\u0435\u043d\u044c",
    "Order canceled": "\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f \u0441\u043a\u0430\u0441\u043e\u0432\u0430\u043d\u043e",
    "Order not approved": "\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f \u043d\u0435 \u0443\u0437\u0433\u043e\u0434\u0436\u0435\u043d\u0435",
    "Others": "\u0406\u043d\u0448\u0435",
    "Paid orders": "\u0421\u043f\u043b\u0430\u0447\u0435\u043d\u0456 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f",
    "PayPal": "PayPal",
    "PayPal Credit": "PayPal \u041a\u0440\u0435\u0434\u0438\u0442",
    "PayPal Pay Later": "PayPal \u041e\u043f\u043b\u0430\u0442\u0438\u0442\u0438 \u043f\u0456\u0437\u043d\u0456\u0448\u0435",
    "PayU": "PayU",
    "Payment method unavailable": "\u0421\u043f\u043e\u0441\u0456\u0431 \u043e\u043f\u043b\u0430\u0442\u0438 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u0438\u0439",
    "Placed orders": "\u0421\u0442\u0432\u043e\u0440\u0435\u043d\u0456 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f",
    "Please enter a quantity for one of the ticket types.": "\u0411\u0443\u0434\u044c \u043b\u0430\u0441\u043a\u0430, \u0432\u0432\u0435\u0434\u0456\u0442\u044c \u043a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0434\u043b\u044f \u043e\u0434\u043d\u043e\u0433\u043e \u0442\u0438\u043f\u0443 \u043a\u0432\u0438\u0442\u043a\u0456\u0432.",
    "Please enter the amount the organizer can keep.": "\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0441\u0443\u043c\u0443, \u044f\u043a\u0443 \u043c\u043e\u0436\u0435 \u0437\u0430\u043b\u0438\u0448\u0438\u0442\u0438 \u043e\u0440\u0433\u0430\u043d\u0456\u0437\u0430\u0442\u043e\u0440.",
    "Powered by pretix": "\u041d\u0430 \u0431\u0430\u0437\u0456 pretix",
    "Press Ctrl-C to copy!": "\u041d\u0430\u0442\u0438\u0441\u043d\u0456\u0442\u044c Ctrl+C \u0449\u043e\u0431 \u0441\u043a\u043e\u043f\u0456\u044e\u0432\u0430\u0442\u0438!",
    "Product": "\u041f\u0440\u043e\u0434\u0443\u043a\u0442",
    "Product variation": "\u0412\u0430\u0440\u0456\u0430\u043d\u0442\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0443",
    "Przelewy24": "Przelewy24",
    "Redeemed": "\u0412\u0438\u043a\u0443\u043f\u043b\u0435\u043d\u043e",
    "Result": "\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442",
    "SEPA Direct Debit": "\u041f\u0440\u044f\u043c\u0438\u0439 \u0434\u0435\u0431\u0435\u0442 SEPA",
    "SOFORT": "SOFORT",
    "Sa": "\u0421\u0431",
    "Saving failed.": "\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0437\u0431\u0435\u0440\u0435\u0433\u0442\u0438.",
    "Scan a ticket or search and press return\u2026": "\u0417\u0456\u0441\u043a\u0430\u043d\u0443\u0439\u0442\u0435 \u043a\u0432\u0438\u0442\u043e\u043a \u0430\u0431\u043e \u0448\u0443\u043a\u0430\u0439\u0442\u0435 \u0442\u0430 \u043d\u0430\u0442\u0438\u0441\u043d\u0456\u0442\u044c \u043f\u043e\u0432\u0435\u0440\u043d\u0435\u043d\u043d\u044f\u2026",
    "Search query": "\u041f\u043e\u0448\u0443\u043a\u043e\u0432\u0438\u0439 \u0437\u0430\u043f\u0438\u0442",
    "Search results": "\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u043f\u043e\u0448\u0443\u043a\u0443",
    "Select a check-in list": "\u0412\u0438\u0431\u0435\u0440\u0456\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a \u0440\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u0457",
    "Selected only": "\u0422\u0456\u043b\u044c\u043a\u0438 \u0432\u0438\u0431\u0440\u0430\u043d\u0456",
    "September": "\u0432\u0435\u0440\u0435\u0441\u0435\u043d\u044c",
    "Su": "\u041d\u0434",
    "Switch check-in list": "\u0417\u043c\u0456\u043d\u0438\u0442\u0438 \u0441\u043f\u0438\u0441\u043e\u043a \u0440\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u0457",
    "Switch direction": "\u0417\u043c\u0456\u043d\u0438\u0442\u0438 \u043d\u0430\u043f\u0440\u044f\u043c\u043e\u043a",
    "Th": "\u0427\u0442",
    "The PDF background file could not be loaded for the following reason:": "\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438 \u0444\u043e\u043d\u043e\u0432\u0438\u0439 \u0444\u0430\u0439\u043b PDF \u0437 \u043d\u0430\u0441\u0442\u0443\u043f\u043d\u043e\u0457 \u043f\u0440\u0438\u0447\u0438\u043d\u0438:",
    "The items in your cart are no longer reserved for you. You can still complete your order as long as they\u2019re available.": "\u0422\u043e\u0432\u0430\u0440\u0438 \u0443 \u0432\u0430\u0448\u043e\u043c\u0443 \u043a\u043e\u0448\u0438\u043a\u0443 \u0431\u0456\u043b\u044c\u0448\u0435 \u043d\u0435 \u0437\u0430\u0440\u0435\u0437\u0435\u0440\u0432\u043e\u0432\u0430\u043d\u0456 \u0434\u043b\u044f \u0432\u0430\u0441. \u0412\u0438 \u0432\u0441\u0435 \u0449\u0435 \u043c\u043e\u0436\u0435\u0442\u0435 \u0437\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u0438 \u0441\u0432\u043e\u0454 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f, \u043f\u043e\u043a\u0438 \u0432\u043e\u043d\u0438 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u0456.",
    "The organizer keeps %(currency)s %(amount)s": "\u041e\u0440\u0433\u0430\u043d\u0456\u0437\u0430\u0442\u043e\u0440 \u0443\u0442\u0440\u0438\u043c\u0443\u0454 %(amount)s %(currency)s",
    "The request took too long. Please try again.": "\u0417\u0430\u043f\u0438\u0442 \u0442\u0440\u0438\u0432\u0430\u0432 \u0437\u0430\u043d\u0430\u0434\u0442\u043e \u0434\u043e\u0432\u0433\u043e. \u0411\u0443\u0434\u044c \u043b\u0430\u0441\u043a\u0430 \u0441\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0449\u0435 \u0440\u0430\u0437.",
    "This ticket is not yet paid. Do you want to continue anyways?": "\u0426\u0435\u0439 \u043a\u0432\u0438\u0442\u043e\u043a \u0449\u0435 \u043d\u0435 \u043e\u043f\u043b\u0430\u0447\u0435\u043d\u0438\u0439. \u0412\u0438 \u0432\u0441\u0435 \u043e\u0434\u043d\u043e \u0445\u043e\u0447\u0435\u0442\u0435 \u043f\u0440\u043e\u0434\u043e\u0432\u0436\u0438\u0442\u0438?",
    "This ticket requires special attention": "\u0426\u0435\u0439 \u043a\u0432\u0438\u0442\u043e\u043a \u0432\u0438\u043c\u0430\u0433\u0430\u0454 \u043e\u0441\u043e\u0431\u043b\u0438\u0432\u043e\u0457 \u0443\u0432\u0430\u0433\u0438",
    "Ticket already used": "\u041a\u0432\u0438\u0442\u043e\u043a \u0443\u0436\u0435 \u0432\u0438\u043a\u043e\u0440\u0438\u0441\u0442\u0430\u043d\u0438\u0439",
    "Ticket blocked": "\u041a\u0432\u0438\u0442\u043e\u043a \u0437\u0430\u0431\u043b\u043e\u043a\u043e\u0432\u0430\u043d\u0438\u0439",
    "Ticket code is ambiguous on list": "\u041a\u043e\u0434 \u043a\u0432\u0438\u0442\u043a\u0430 \u0443 \u0441\u043f\u0438\u0441\u043a\u0443 \u043d\u0435 \u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u0438\u0439",
    "Ticket code revoked/changed": "\u041a\u043e\u0434 \u043a\u0432\u0438\u0442\u043a\u0430 \u0432\u0456\u0434\u043a\u043b\u0438\u043a\u0430\u043d\u0438\u0439/\u0437\u043c\u0456\u043d\u0435\u043d\u0438\u0439",
    "Ticket design": "\u0414\u0438\u0437\u0430\u0439\u043d \u043a\u0432\u0438\u0442\u043a\u0430",
    "Ticket not paid": "\u041a\u0432\u0438\u0442\u043e\u043a \u043d\u0435 \u043e\u043f\u043b\u0430\u0447\u0435\u043d\u043e",
    "Ticket not valid at this time": "\u041a\u0432\u0438\u0442\u043e\u043a \u0437\u0430\u0440\u0430\u0437 \u043d\u0435 \u0434\u0456\u0439\u0441\u043d\u0438\u0439",
    "Ticket type not allowed here": "\u0422\u0438\u043f \u043a\u0432\u0438\u0442\u043a\u0430 \u0442\u0443\u0442 \u0437\u0430\u0431\u043e\u0440\u043e\u043d\u0435\u043d\u0438\u0439",
    "Time zone:": "\u0427\u0430\u0441\u043e\u0432\u0438\u0439 \u043f\u043e\u044f\u0441:",
    "Tolerance (minutes)": "\u0412\u0456\u0434\u0445\u0438\u043b\u0435\u043d\u043d\u044f (\u0445\u0432\u0438\u043b.)",
    "Total": "\u0417\u0430\u0433\u0430\u043b\u043e\u043c",
    "Total revenue": "\u0417\u0430\u0433\u0430\u043b\u044c\u043d\u0438\u0439 \u043f\u0440\u0438\u0431\u0443\u0442\u043e\u043a",
    "Trustly": "Trustly",
    "Tu": "\u0412\u0442",
    "Unknown error.": "\u041d\u0435\u0432\u0456\u0434\u043e\u043c\u0430 \u043f\u043e\u043c\u0438\u043b\u043a\u0430.",
    "Unknown ticket": "\u041a\u0432\u0438\u0442\u043e\u043a \u043d\u0435 \u0437\u043d\u0430\u0439\u0434\u0435\u043d\u043e",
    "Unpaid": "\u041d\u0435\u043e\u043f\u043b\u0430\u0447\u0435\u043do",
    "Use a different name internally": "\u0412\u0438\u043a\u043e\u0440\u0438\u0441\u0442\u0430\u0439\u0442\u0435 \u0456\u043d\u0448\u0443 \u0432\u043d\u0443\u0442\u0440\u0456\u0448\u043d\u044e \u043d\u0430\u0437\u0432\u0443",
    "Valid": "\u0414\u0456\u0439\u0441\u043d\u0438\u0439",
    "Valid Tickets": "\u0414\u0456\u0439\u0441\u043d\u0456 \u043a\u0432\u0438\u0442\u043a\u0438",
    "Valid ticket": "\u0414\u0456\u0439\u0441\u043d\u0438\u0439 \u043a\u0432\u0438\u0442\u043e\u043a",
    "Venmo": "Venmo",
    "Verkkopankki": "Verkkopankki",
    "We": "\u0421\u0440",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "\u0417\u0430\u0440\u0430\u0437 \u043c\u0438 \u043d\u0430\u0434\u0441\u0438\u043b\u0430\u0454\u043c\u043e \u0412\u0430\u0448 \u0437\u0430\u043f\u0438\u0442 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440. \u042f\u043a\u0449\u043e \u0446\u0435 \u0437\u0430\u0439\u043c\u0435 \u0431\u0456\u043b\u044c\u0448\u0435 \u043e\u0434\u043d\u0456\u0454\u0457 \u0445\u0432\u0438\u043b\u0438\u043d\u0438, \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u0442\u0435 \u043f\u0456\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044f \u0434\u043e \u0406\u043d\u0442\u0435\u0440\u043d\u0435\u0442\u0443, \u0430 \u043f\u043e\u0442\u0456\u043c \u043f\u0435\u0440\u0435\u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0442\u0435 \u0446\u044e \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0443 \u0442\u0430 \u043f\u043e\u0432\u0442\u043e\u0440\u0456\u0442\u044c \u0441\u043f\u0440\u043e\u0431\u0443.",
    "We are processing your request \u2026": "\u041c\u0438 \u043e\u0431\u0440\u043e\u0431\u043b\u044f\u0454\u043c\u043e \u0432\u0430\u0448 \u0437\u0430\u043f\u0438\u0442\u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "\u041d\u0435 \u0432\u0434\u0430\u0454\u0442\u044c\u0441\u044f \u0437\u0432'\u044f\u0437\u0430\u0442\u0438\u0441\u044f \u0456\u0437 \u0441\u0435\u0440\u0432\u0435\u0440\u043e\u043c, \u043f\u043e\u0432\u0442\u043e\u0440\u044e\u0454\u043c\u043e \u0441\u043f\u0440\u043e\u0431\u0438. \u041a\u043e\u0434 \u043e\u0441\u0442\u0430\u043d\u043d\u044c\u043e\u0457 \u043f\u043e\u043c\u0438\u043b\u043a\u0438: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "\u041d\u0430\u0440\u0430\u0437\u0456 \u043c\u0438 \u043d\u0435 \u043c\u043e\u0436\u0435\u043c\u043e \u043f\u0456\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u0438\u0441\u044f \u0434\u043e \u0441\u0435\u0440\u0432\u0435\u0440\u0430. \u0411\u0443\u0434\u044c \u043b\u0430\u0441\u043a\u0430 \u0441\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0449\u0435 \u0440\u0430\u0437. \u041a\u043e\u0434 \u043f\u043e\u043c\u0438\u043b\u043a\u0438: {code}",
    "WeChat Pay": "WeChat Pay",
    "Yes": "\u0422\u0430\u043a",
    "You get %(currency)s %(amount)s back": "\u0412\u0438 \u043e\u0442\u0440\u0438\u043c\u0430\u0454\u0442\u0435 \u0432 \u043f\u043e\u0432\u0435\u0440\u043d\u0435\u043d\u043d\u0456 %(amount)s %(currency)s",
    "You have unsaved changes!": "\u0423 \u0432\u0430\u0441 \u0454 \u043d\u0435\u0437\u0431\u0435\u0440\u0435\u0436\u0435\u043d\u0456 \u0437\u043c\u0456\u043d\u0438!",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "\u0412\u0430\u0448 \u043a\u043e\u043b\u0456\u0440 \u043c\u0430\u0454 \u043d\u0438\u0437\u044c\u043a\u0443 \u043a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u0456\u0441\u0442\u044c \u0434\u043b\u044f \u0442\u0435\u043a\u0441\u0442\u0443 \u043d\u0430 \u0431\u0456\u043b\u043e\u043c\u0443 \u0442\u043b\u0456, \u0431\u0443\u0434\u044c \u043b\u0430\u0441\u043a\u0430, \u0432\u0438\u0431\u0435\u0440\u0456\u0442\u044c \u0442\u0435\u043c\u043d\u0456\u0448\u0438\u0439 \u0432\u0456\u0434\u0442\u0456\u043d\u043e\u043a.",
    "Your color has decent contrast and is probably good-enough to read!": "\u0412\u0430\u0448 \u043a\u043e\u043b\u0456\u0440 \u043c\u0430\u0454 \u0434\u043e\u0441\u0442\u0430\u0442\u043d\u044e \u043a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u0456\u0441\u0442\u044c \u0456, \u0439\u043c\u043e\u0432\u0456\u0440\u043d\u043e, \u0446\u0456\u043b\u043a\u043e\u043c \u043f\u0456\u0434\u0445\u043e\u0434\u0438\u0442\u044c \u0434\u043b\u044f \u0447\u0438\u0442\u0430\u043d\u043d\u044f!",
    "Your color has great contrast and is very easy to read!": "\u0412\u0430\u0448 \u043a\u043e\u043b\u0456\u0440 \u043c\u0430\u0454 \u0432\u0435\u043b\u0438\u043a\u0438\u0439 \u043a\u043e\u043d\u0442\u0440\u0430\u0441\u0442 \u0456 \u0439\u043e\u0433\u043e \u0434\u0443\u0436\u0435 \u043b\u0435\u0433\u043a\u043e \u0447\u0438\u0442\u0430\u0442\u0438!",
    "Your local time:": "\u0412\u0430\u0448 \u043c\u0456\u0441\u0446\u0435\u0432\u0438\u0439 \u0447\u0430\u0441:",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "\u0412\u0430\u0448 \u0437\u0430\u043f\u0438\u0442 \u043d\u0430\u0434\u0456\u0439\u0448\u043e\u0432 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440, \u0430\u043b\u0435 \u0432\u0441\u0435 \u0449\u0435 \u043f\u0435\u0440\u0435\u0431\u0443\u0432\u0430\u0454 \u0432 \u043e\u0447\u0456\u043a\u0443\u0432\u0430\u043d\u043d\u0456 \u043e\u0431\u0440\u043e\u0431\u043a\u0438. \u042f\u043a\u0449\u043e \u0446\u0435 \u0437\u0430\u0439\u043c\u0435 \u0431\u0456\u043b\u044c\u0448\u0435 \u0434\u0432\u043e\u0445 \u0445\u0432\u0438\u043b\u0438\u043d, \u0431\u0443\u0434\u044c \u043b\u0430\u0441\u043a\u0430, \u0437\u0432'\u044f\u0436\u0456\u0442\u044c\u0441\u044f \u0437 \u043d\u0430\u043c\u0438 \u0430\u0431\u043e \u043f\u043e\u0432\u0435\u0440\u043d\u0456\u0442\u044c\u0441\u044f \u043d\u0430\u0437\u0430\u0434 \u0443 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0456 \u0442\u0430 \u043f\u043e\u0432\u0442\u043e\u0440\u0456\u0442\u044c \u0437\u0430\u043f\u0438\u0442.",
    "Your request has been queued on the server and will soon be processed.": "\u0412\u0430\u0448 \u0437\u0430\u043f\u0438\u0442 \u043f\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043e \u0432 \u0447\u0435\u0440\u0433\u0443 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0456 \u0456 \u043d\u0435\u0437\u0430\u0431\u0430\u0440\u043e\u043c \u0431\u0443\u0434\u0435 \u043e\u0431\u0440\u043e\u0431\u043b\u0435\u043d\u043e.",
    "Your request is currently being processed. Depending on the size of your event, this might take up to a few minutes.": "\u0412\u0430\u0448 \u0437\u0430\u043f\u0438\u0442 \u043d\u0430\u0440\u0430\u0437\u0456 \u043e\u0431\u0440\u043e\u0431\u043b\u044f\u0454\u0442\u044c\u0441\u044f. \u0417\u0430\u043b\u0435\u0436\u043d\u043e \u0432\u0456\u0434 \u043c\u0430\u0441\u0448\u0442\u0430\u0431\u0443 \u0432\u0430\u0448\u043e\u0457 \u043f\u043e\u0434\u0456\u0457 \u0446\u0435 \u043c\u043e\u0436\u0435 \u0437\u0430\u0439\u043d\u044f\u0442\u0438 \u0434\u043e \u043a\u0456\u043b\u044c\u043a\u043e\u0445 \u0445\u0432\u0438\u043b\u0438\u043d.",
    "Zimpler": "Zimpler",
    "close": "\u0417\u0430\u043a\u0440\u0438\u0442\u0438",
    "custom date and time": "\u0432\u043b\u0430\u0441\u043d\u0456 \u0434\u0430\u0442\u0430 \u0442\u0430 \u0447\u0430\u0441",
    "custom time": "\u0432\u043b\u0430\u0441\u043d\u0438\u0439 \u0447\u0430\u0441",
    "entry_status\u0004absent": "\u0432\u0456\u0434\u0441\u0443\u0442\u043d\u0456\u0439",
    "entry_status\u0004present": "\u043f\u0440\u0438\u0441\u0443\u0442\u043d\u0456\u0439",
    "eps": "eps",
    "giropay": "giropay",
    "iDEAL": "iDEAL",
    "is after": "\u0454 \u043f\u0456\u0441\u043b\u044f",
    "is before": "\u0454 \u0440\u0430\u043d\u0456\u0448\u0435",
    "is one of": "\u0454 \u043e\u0434\u043d\u0438\u043c \u0456\u0437",
    "required": "\u043e\u0431\u043e\u0432'\u044f\u0437\u043a\u043e\u0432\u0435",
    "widget\u0004Back": "\u041d\u0430\u0437\u0430\u0434",
    "widget\u0004Buy": "\u041a\u0443\u043f\u0438\u0442\u0438",
    "widget\u0004Choose a different date": "\u041e\u0431\u0440\u0430\u0442\u0438 \u0456\u043d\u0448\u0443 \u0434\u0430\u0442\u0443",
    "widget\u0004Choose a different event": "\u041e\u0431\u0440\u0430\u0442\u0438 \u0456\u043d\u0448\u0443 \u043f\u043e\u0434\u0456\u044e",
    "widget\u0004Close": "\u0417\u0430\u043a\u0440\u0438\u0442\u0438",
    "widget\u0004Close ticket shop": "\u0417\u0430\u043a\u0440\u0438\u0442\u0438 \u043a\u0432\u0438\u0442\u043a\u043e\u0432\u0443 \u043a\u0440\u0430\u043c\u043d\u0438\u0446\u044e",
    "widget\u0004Continue": "\u041f\u0440\u043e\u0434\u043e\u0432\u0436\u0438\u0442\u0438",
    "widget\u0004Currently not available": "\u0417\u0430\u0440\u0430\u0437 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u043e",
    "widget\u0004Decrease quantity": "\u0417\u043c\u0435\u043d\u0448\u0438\u0442\u0438 \u043a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c",
    "widget\u0004FREE": "\u0411\u0415\u0417\u041a\u041e\u0428\u0422\u041e\u0412\u041d\u041e",
    "widget\u0004Hide variants": "\u0421\u0445\u043e\u0432\u0430\u0442\u0438 \u0432\u0430\u0440\u0456\u0430\u043d\u0442\u0438",
    "widget\u0004Increase quantity": "\u0417\u0431\u0456\u043b\u044c\u0448\u0438\u0442\u0438 \u043a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c",
    "widget\u0004Load more": "\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438 \u0431\u0456\u043b\u044c\u0448\u0435",
    "widget\u0004Next month": "\u041d\u0430\u0441\u0442\u0443\u043f\u043d\u0438\u0439 \u043c\u0456\u0441\u044f\u0446\u044c",
    "widget\u0004Next week": "\u041d\u0430\u0441\u0442\u0443\u043f\u043d\u0438\u0439 \u0442\u0438\u0436\u0434\u0435\u043d\u044c",
    "widget\u0004Not available anymore": "\u0411\u0456\u043b\u044c\u0448\u0435 \u043d\u0435 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u043e",
    "widget\u0004Not yet available": "\u0417\u0430\u0440\u0430\u0437 \u043d\u0435 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u043e",
    "widget\u0004Only available with a voucher": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u043b\u0438\u0448\u0435 \u0437 \u0432\u0430\u0443\u0447\u0435\u0440\u043e\u043c",
    "widget\u0004Open seat selection": "\u0414\u043e\u0432\u0456\u043b\u044c\u043d\u0438\u0439 \u0432\u0438\u0431\u0456\u0440 \u043c\u0456\u0441\u0446\u044f",
    "widget\u0004Open ticket shop": "\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438 \u043a\u0430\u0441\u0443",
    "widget\u0004Previous month": "\u041f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0439 \u043c\u0456\u0441\u044f\u0446\u044c",
    "widget\u0004Previous week": "\u041f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u0456\u0439 \u0442\u0438\u0436\u0434\u0435\u043d\u044c",
    "widget\u0004Price": "\u0426\u0456\u043d\u0430",
    "widget\u0004Quantity": "\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c",
    "widget\u0004Redeem": "\u0412\u0438\u043a\u043e\u0440\u0438\u0441\u0442\u0430\u0442\u0438",
    "widget\u0004Redeem a voucher": "\u0412\u0438\u043a\u043e\u0440\u0438\u0441\u0442\u0430\u0442\u0438 \u043f\u0440\u043e\u043c\u043e\u043a\u043e\u0434",
    "widget\u0004Register": "\u0417\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u0443\u0432\u0430\u0442\u0438\u0441\u044c",
    "widget\u0004Reserved": "\u0417\u0430\u0440\u0435\u0437\u0435\u0440\u0432\u043e\u0432\u0430\u043d\u043e",
    "widget\u0004Resume checkout": "\u0412\u0456\u0434\u043d\u043e\u0432\u0438\u0442\u0438 \u043e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u043d\u044f \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f",
    "widget\u0004Select": "\u0412\u0438\u0431\u0435\u0440\u0456\u0442\u044c",
    "widget\u0004Select %s": "\u0412\u0438\u0431\u0435\u0440\u0456\u0442\u044c %s",
    "widget\u0004Select variant %s": "\u0412\u0438\u0431\u0435\u0440\u0456\u0442\u044c \u0432\u0430\u0440\u0456\u0430\u043d\u0442 %s",
    "widget\u0004Show variants": "\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u0438 \u0432\u0430\u0440\u0456\u0430\u043d\u0442\u0438",
    "widget\u0004Sold out": "\u0420\u043e\u0437\u043f\u0440\u043e\u0434\u0430\u043d\u043e",
    "widget\u0004Some or all ticket categories are currently sold out. If you want, you can add yourself to the waiting list. We will then notify if seats are available again.": "\u0414\u0435\u044f\u043a\u0456 \u0430\u0431\u043e \u0432\u0441\u0456 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457 \u043a\u0432\u0438\u0442\u043a\u0456\u0432 \u0437\u0430\u0440\u0430\u0437 \u0440\u043e\u0437\u043f\u0440\u043e\u0434\u0430\u043d\u0456. \u042f\u043a\u0449\u043e \u0445\u043e\u0447\u0435\u0442\u0435, \u043c\u043e\u0436\u0435\u0442\u0435 \u0434\u043e\u0434\u0430\u0442\u0438\u0441\u044f \u0434\u043e \u0441\u043f\u0438\u0441\u043a\u0443 \u043e\u0447\u0456\u043a\u0443\u0432\u0430\u043d\u043d\u044f. \u0422\u043e\u0434\u0456 \u043c\u0438 \u0412\u0430\u043c \u043f\u043e\u0432\u0456\u0434\u043e\u043c\u0438\u043c\u043e, \u043a\u043e\u043b\u0438 \u043c\u0456\u0441\u0446\u044f \u0437\u043d\u043e\u0432\u0443 \u0431\u0443\u0434\u0443\u0442\u044c \u0432\u0456\u043b\u044c\u043d\u0456.",
    "widget\u0004The cart could not be created. Please try again later": "\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0441\u0442\u0432\u043e\u0440\u0438\u0442\u0438 \u043a\u043e\u0448\u0438\u043a. \u0411\u0443\u0434\u044c-\u043b\u0430\u0441\u043a\u0430 \u0441\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u043f\u0456\u0437\u043d\u0456\u0448\u0435",
    "widget\u0004The ticket shop could not be loaded.": "\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438 \u043a\u0432\u0438\u0442\u043a\u043e\u0432\u0443 \u043a\u0440\u0430\u043c\u043d\u0438\u0446\u044e.",
    "widget\u0004There are currently a lot of users in this ticket shop. Please open the shop in a new tab to continue.": "\u0417\u0430\u0440\u0430\u0437 \u0443 \u0446\u0456\u0439 \u043a\u0430\u0441\u0456 \u0431\u0430\u0433\u0430\u0442\u043e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456\u0432. \u0429\u043e\u0431 \u043f\u0440\u043e\u0434\u043e\u0432\u0436\u0438\u0442\u0438, \u0432\u0456\u0434\u043a\u0440\u0438\u0439\u0442\u0435 \u0432\u0456\u043a\u043d\u043e \u043a\u0432\u0438\u0442\u043a\u0456\u0432 \u0443 \u043d\u043e\u0432\u0456\u0439 \u0432\u043a\u043b\u0430\u0434\u0446\u0456.",
    "widget\u0004Voucher code": "\u041f\u0440\u043e\u043c\u043e\u043a\u043e\u0434",
    "widget\u0004Waiting list": "C\u043f\u0438\u0441\u043e\u043a \u043e\u0447\u0456\u043a\u0443\u0432\u0430\u043d\u043d\u044f",
    "widget\u0004We could not create your cart, since there are currently too many users in this ticket shop. Please click \"Continue\" to retry in a new tab.": "\u041d\u0430\u043c \u043d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0441\u0442\u0432\u043e\u0440\u0438\u0442\u0438 \u0432\u0430\u0448 \u043a\u043e\u0448\u0438\u043a, \u043e\u0441\u043a\u0456\u043b\u044c\u043a\u0438 \u0437\u0430\u0440\u0430\u0437 \u0443 \u0446\u0456\u0439 \u043a\u0432\u0438\u0442\u043a\u043e\u0432\u0456\u0439 \u043a\u0440\u0430\u043c\u043d\u0438\u0446\u0456 \u0437\u0430\u043d\u0430\u0434\u0442\u043e \u0431\u0430\u0433\u0430\u0442\u043e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456\u0432. \u041d\u0430\u0442\u0438\u0441\u043d\u0456\u0442\u044c \u00ab\u041f\u0440\u043e\u0434\u043e\u0432\u0436\u0438\u0442\u0438\u00bb, \u0449\u043e\u0431 \u043f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0438 \u0441\u043f\u0440\u043e\u0431\u0443 \u0443 \u043d\u043e\u0432\u0456\u0439 \u0432\u043a\u043b\u0430\u0434\u0446\u0456.",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "\u0417\u0430\u0440\u0430\u0437 \u0443 \u0432\u0430\u0441 \u0454 \u0430\u043a\u0442\u0438\u0432\u043d\u0438\u0439 \u043a\u043e\u0448\u0438\u043a \u0434\u043b\u044f \u0446\u0456\u0454\u0457 \u043f\u043e\u0434\u0456\u0457. \u042f\u043a\u0449\u043e \u0432\u0438 \u0432\u0438\u0431\u0435\u0440\u0435\u0442\u0435 \u0431\u0456\u043b\u044c\u0448\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0456\u0432, \u0432\u043e\u043d\u0438 \u0431\u0443\u0434\u0443\u0442\u044c \u0434\u043e\u0434\u0430\u043d\u0456 \u0434\u043e \u0432\u0430\u0448\u043e\u0433\u043e \u043d\u0430\u044f\u0432\u043d\u043e\u0433\u043e \u043a\u043e\u0448\u0438\u043a\u0430.",
    "widget\u0004currently available: %s": "\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0437\u0430\u0440\u0430\u0437: %s",
    "widget\u0004from %(currency)s %(price)s": "\u0432\u0456\u0434 %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "\u0432\u043a\u043b.%(rate)s% %(taxname)s",
    "widget\u0004incl. taxes": "\u0432\u0440\u0430\u0445\u043e\u0432\u0443\u044e\u0447\u0438 \u043f\u043e\u0434\u0430\u0442\u043a\u0438",
    "widget\u0004minimum amount to order: %s": "\u043c\u0456\u043d\u0456\u043c\u0430\u043b\u044c\u043d\u0430 \u0441\u0443\u043c\u0430 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f:%s",
    "widget\u0004plus %(rate)s% %(taxname)s": "\u043f\u043b\u044e\u0441%(rate)s% %(taxname)s",
    "widget\u0004plus taxes": "\u043f\u043b\u044e\u0441 \u043f\u043e\u0434\u0430\u0442\u043a\u0438"
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "d E Y \u0440. H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%d %B %Y %H:%M:%S",
      "%d %B %Y %H:%M:%S.%f",
      "%d %B %Y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "d E Y \u0440.",
    "DATE_INPUT_FORMATS": [
      "%d.%m.%Y",
      "%d %B %Y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "d F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d.m.Y H:i",
    "SHORT_DATE_FORMAT": "d.m.Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};

