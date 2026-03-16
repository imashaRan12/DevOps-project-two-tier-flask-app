document.addEventListener("DOMContentLoaded", function () {
  console.log("Project Tracker Loaded");

  let rows = document.querySelectorAll("table tr");

  rows.forEach(function (row) {
    row.addEventListener("mouseover", function () {
      row.style.backgroundColor = "#eef2ff";
    });

    row.addEventListener("mouseout", function () {
      row.style.backgroundColor = "";
    });
  });
});
