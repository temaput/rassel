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
  "didConcent",
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
function myFunction() {
  var activeSheet = SpreadsheetApp.getActiveSheet();
  var selection = activeSheet.getSelection();
  var data = activeSheet.getDataRange().getValues();
  const row = selection.getCurrentCell().getRow();

  const rowData = data[row - 1];
  if (rowData) {
    let survey = {};
    for (let i = 0; i < rowData.length; i++) {
      survey[FNAMES[i]] = rowData[i];
    }
    Logger.log(survey);

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
    Logger.log(response);
  }
}
function dateStringToUTC(d) {
    const localDate = new Date(d);
    return Date.UTC(localDate.getFullYear(), localDate.getMonth(), localDate.getDate(), localDate.getHours(), localDate.getMinutes(), localDate.getSeconds())
}
function transformDate(d) {
    return new Date(dateStringToUTC(d)).toISOString();
}
