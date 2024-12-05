
// Obtén el contenido de 'reports'
var rawText = document.getElementById('reports').textContent;
// Primer parseo: convierte la cadena con comillas escapadas en una cadena válida
var parsedString = JSON.parse(rawText);
// Segundo parseo: convierte la cadena JSON en un objeto
var pdfReports = JSON.parse(parsedString);
var request_id = pdfReports.request_id 

    if (pdfReports.check_rep_liq) {
        var baseUrl = window.location.origin;
        var reportUrl =baseUrl + "/cesantias/reporte/?report_name=Liquidacion&object_id= " + request_id;
        window.open(reportUrl);  // Redirige a la URL directamente
    }
    if (pdfReports.check_rep_cdp) {
        var baseUrl = window.location.origin;
        var reportUrl =baseUrl + "/cesantias/reporte/?report_name=Solicitud_CDP&object_id= " + request_id;
        window.open(reportUrl);  // Redirige a la URL directamente
    }
    if (pdfReports.check_rep_rso) {
        var baseUrl = window.location.origin;
        var reportUrl =baseUrl + "/cesantias/reporte/?report_name=Emision_Resolucion&object_id= " + request_id;
        window.open(reportUrl);  // Redirige a la URL directamente
    }
    if (pdfReports.check_rep_rpc) {
        var baseUrl = window.location.origin;
        var reportUrl =baseUrl + "/cesantias/reporte/?report_name=Solicitud_RPC&object_id= " + request_id;
        window.open(reportUrl);  // Redirige a la URL directamente
    }



