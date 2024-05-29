$(document).ready(function () {
  $("#scraperForm").on("submit", function (event) {
    $("#scraperForm").hide();
    $("#loading").show();
    event.preventDefault();
    const hotelName = $("#hotel").val();
    const apiRoute = $('input[name="api"]:checked').val();
    let apiUrl;

    if (apiRoute === "all") {
      apiUrl = "/hotels";
    } else {
      apiUrl = `/hotels/${apiRoute}`;
    }

    $.ajax({
      url: apiUrl,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ hotel: hotelName }),
      success: function (data) {
        let result = "<h2>Results</h2>";
        result += `<p>Date & Time: ${data["Date & Time"]}</p>`;
        result += `<p>Hotel Name: ${data["Hotel Name"]}</p>`;

        if (apiRoute === "tiket" || apiRoute === "all") {
          result += `<p>Tiket Price: IDR ${data["Tiket Price"]}</p>`;
        }
        if (apiRoute === "traveloka" || apiRoute === "all") {
          result += `<p>Traveloka Price: IDR ${data["Traveloka Price"]}</p>`;
        }
        if (apiRoute === "agoda" || apiRoute === "all") {
          result += `<p>Agoda Price: IDR ${data["Agoda Price"]}</p>`;
        }

        $("#results").html(result);
      },
      error: function (error) {
        console.error("Error:", error);
      },
      complete: function () {
        $("#loading").hide();
        $("#scraperForm").show();
        $("#scraperForm").trigger("reset");
      },
    });
  });
});
