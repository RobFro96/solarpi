function onload() {
    document.getElementById("datepicker").valueAsDate = new Date();
    update_plot();
}

function update_plot() {
    document.getElementById("content_img").src = "";

    let visu = document.getElementById("visu_select").value;
    let date = document.getElementById("datepicker").valueAsDate

    let datestring = formatDateToYYMMDD(date)
    let always_uptodate = "?t=" + Date.now();

    document.getElementById("content_img").src = "/visu/" + visu + "/" + datestring + always_uptodate;
}

function formatDateToYYMMDD(date) {
    // Extract year, month, and day components from the Date object
    let year = date.getFullYear().toString().slice(-2); // Get last 2 digits of the year
    let month = (date.getMonth() + 1).toString(); // Month is zero-based, so add 1
    let day = date.getDate().toString();
  
    // Pad month and day with leading zeros if necessary
    if (month.length === 1) {
      month = '0' + month;
    }
    if (day.length === 1) {
      day = '0' + day;
    }
  
    // Concatenate year, month, and day with no separators
    return year + month + day;
  }