var req;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/klev/get-devices", true);
    //req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    //req.setRequestHeader('X-CSRFToken', csrfcookie());
    //req.onload = callback;
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
    //var list = document.getElementById("devices");
    //while (list.hasChildNodes()) {
    //    list.removeChild(list.firstChild);
    //}

    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var devices = JSON.parse(req.responseText);
    var row = document.createElement("row");
    //row.innerHTML = devices[0]["fields"]["deviceName"];
    // Adds each new devices item to the list
    var string = "";
    var string2 = "";
    //var string = "card"+devices[i]["fields"]["trained"];
    //$("h6").css("font-style", "italic"); // Not permanent, just syntax for jquery

    // Ajax request to update card color. NOT CORRECT, Look at syntax though
    for (var i = 0; i < devices.length; ++i) {
      string = "#card_"+devices[i]["fields"]["deviceName"];
      if (devices[i]["fields"]["deviceState"] == 'ON'){
        $(string).removeClass("card small yellow");
        $(string).removeClass("card small red");
        $(string).removeClass("card small blue");
        $(string).removeClass("card small green");
        string2 = "#"+devices[i]["fields"]["deviceName"]+"_deviceState";
        $(string2).text("State: On");
        $(string).addClass("card small green");
      }
      if (devices[i]["fields"]["deviceState"] == 'OFF'){
        $(string).removeClass("card small yellow");
        $(string).removeClass("card small red");
        $(string).removeClass("card small blue");
        $(string).removeClass("card small green");
        string2 = "#"+devices[i]["fields"]["deviceName"]+"_deviceState";
        $(string2).text("State: Off");
        $(string).addClass("card small red");
      }
      if (devices[i]["fields"]["deviceState"] == 'field value'){
        $(string).removeClass("card small yellow");
        $(string).removeClass("card small red");
        $(string).removeClass("card small blue");
        $(string).removeClass("card small green");
        string2 = "#"+devices[i]["fields"]["deviceName"]+"_deviceState";
        $(string2).text("State: Off");
        $(string).addClass("card small red");
      }
    }

    

}
    /*
  

  #################
  ## All of this is Junk
  #################
      string = "";
      if (devices[i]["fields"]["trained"] == 0) {
          string += "<div class=\"card small grey\">";
        }
      string += "<div class=\"col s3\">";
      if (devices[i]["fields"]["trained"] == 0) {
          string += "<div class=\"card small grey\">";
        }
      else {
        if (devices[i]["fields"]["deviceState"] == 'ON')
          string += "<div class=\"card small green\">";
        else if ((devices[i]["fields"]["deviceState"] == 'OFF')) {
          string += "<div class=\"card small red\">";
        }
        else
          string += "<div class=\"card small yellow\">";
      }
      string += "<div class=\"card-content\"><span class=\"card-title activator white-text text-darken-4\">";
      string += devices[i]["fields"]["deviceName"];
      string += "<i class=\"mdi-navigation-more-vert right\"></i></span>";
      string += "<p><a href=\"#\">Visualize</a></p></div>";
      if (devices[i]["fields"]["trained"] == 0) {
        string += "<div class = \"center-align\">";
        string += "<form action=\"{%url 'trainDevice' %}\" method=\"post\">";
        string += "<input type=\"hidden\" name=\"Device\" value=";
        string += devices[i]["fields"]["deviceName"];
        string += "><button class=\"waves-effect waves-light btn\" type=\"submit\" name=\"action\">Train Now! </button>";
        string += "{% csrf_token %}</form></div>";
      }
      /*
      string += "<div class=\"card-reveal\">";
      string += "<span class=\"card-title grey-text text-darken-4\">";
      string += devices[i]["fields"]["deviceName"];
      string += "<i class=\"mdi-navigation-close right\"></i></span>"; 
      string += "<br> <br>";         
      string += "<h6 class=\"center-align\"> Make: ";
      string += devices[i]["fields"]["make"];
      string += "</h6>";
      string += "<h6 class=\"center-align\"> Model: ";
      string += devices[i]["fields"]["modelNum"];
      string += "</h6>";
      string += "<h6 class=\"center-align\"> Location: ";
      string += devices[i]["fields"]["location"];
      string += "</h6>";
      if (devices[i]["fields"]["trained"] == "1") {
          string += "<h6 class=\"center-align\"> Device is Trained </h6>";
          string += "<h6 class=\"center-align\"> State:"; 
          string += devices[i]["fields"]["deviceState"];
          string += "</h6> </div>";
      }
      else {
        string += "<h6 class=\"center-align\"> Device is Untrained! </h6> <div class = \"center-align\"> ";
        string += "<form action=\"{%url 'trainDevice' %}\" method=\"post\">";
        string += "<input type=\"hidden\" name=\"Device\" value=";
        string += devices[i]["fields"]["deviceName"];
        string += "> <button class=\"waves-effect waves-light btn\" type=\"submit\""
        string += "name=\"action\">Train Now! </a> {% csrf_token %} </form>";
        string += "</div>";
      }
      
      string += "</div></div>";
      row.innerHTML += string;
    }/*
    list.appendChild(row);
   



        // Extracts the item id and text from the response
        //var id = items[i]["pk"];  // pk is "primary key", the id
        //var itemText = items[i]["fields"]["text"];
  
        // Builds a new HTML list item for the todo-list item
        //var newItem = document.createElement("li");
        //newItem.innerHTML = "<a href=\"/shared-todo-list/delete-item/" + id + "\">X</a> " + itemText;
        // Adds the todo-list item to the HTML list
        //list.appendChild(newItem);
    
    
}
var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
*/
// causes the sendRequest function to run every 10 seconds
window.setInterval(sendRequest, 100);
