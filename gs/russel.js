const FNAMES = [
  "startTime",
  "endTime",
  "firstName",
  "lastName",
  "mob",
  "email",
  "testingType",
  "testingCalendar",
  "appointmentPrice",
  "isPaid",
  "paidAmount",
  "certificateCode",
  "notes",
  "scheduledAt",
  "label",
  "scheduledBy",
  "address",
  "city",
  "state",
  "zip",
  "sex",
  "dob",
  "race",
  "ethnicity",
  "insuranceCompany",
  "subscriberName",
  "subscriberDOB",
  "subscriberID",
  "subscriberGroup",
  "claimsAddress",
  "insurancePhone",
  "isEmployedInHealthcare",
  "isFirstCOVIDTest",
  "testedPositive",
  "positiveTestDate",
  "haveSymptoms",
  "symptomsOnsetDate",
  "symptomsDescription",
  "isPregnant",
  "isCongregateCareResident",
  "didConsent",
  "appointmentId",

  "middleName",
  "socSec",
  "mob2",
  "country",
  "country2",
  "guardianFirstName",
  "guardianLastName",
  "guardianMiddleName",
  "occupation",
  "employer",
  "employerAddress1",
  "employerAddress2",
  "insuranceCity",
  "subscriberRelation",
  "subscriberRelationOther",
];
function fetchSurveyData() {
  var activeSheet = SpreadsheetApp.getActiveSheet();
  var selection = activeSheet.getSelection();
  var data = activeSheet.getDataRange().getValues();
  const row = selection.getCurrentCell().getRow();

  const rowData = data[row - 1];
  let hasName = false;
  if (rowData) {
    let survey = {};
    for (let i = 0; i < rowData.length; i++) {
      survey[FNAMES[i]] = rowData[i];
      if (FNAMES[i] === "firstName" && !!rowData[i]) {
        hasName = true;
      }
    }
    Logger.log(survey);
    if (hasName) {
      return survey;
    }
    
  }
}

function fetchPDF(survey) {
  const options = {
    method: "post",
    contentType: "application/json",
    // Convert the JavaScript object to a JSON string.
    payload: JSON.stringify({ survey }),
  };

  const response = UrlFetchApp.fetch(
    "https://us-central1-avid-winter-298813.cloudfunctions.net/survey_pdf",
    options
  );
  var blob = response.getAs("application/pdf");
  return blob.getBytes();
}

function onOpen() {
  SpreadsheetApp.getUi() // Or DocumentApp or SlidesApp or FormApp.
    .createMenu("PDF Form")
    .addItem("Print Form", "showDialog")
    .addToUi();
}

function showDialog() {
  var htmlTemplate = HtmlService.createTemplateFromFile("Page");
  const ui =  SpreadsheetApp.getUi();
  const survey = fetchSurveyData();
  if (!survey) {
      ui.alert("Please select the record! No data was found for current selection.")
    return;
  };
  htmlTemplate.survey = JSON.stringify(survey);
  var html = htmlTemplate.evaluate().setWidth(400).setHeight(300);

  // Or DocumentApp or SlidesApp or FormApp.
    ui.showModalDialog(html, "Print Form");
}
