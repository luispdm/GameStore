/**
 * Created by giovanni on 14/02/2016.
 */

/**
 * Format a date using a parse in order to be compatible for multiple browsers
 */

function formatDate(value){
        var monthNames = [
          "January", "February", "March",
          "April", "May", "June", "July",
          "August", "September", "October",
          "November", "December"
        ];

        //var date = new Date(value);

        var date;
        var dateStr=value; //returned from mysql timestamp/datetime field
        var a=dateStr.split(" ");
        var d=a[0].split("-");
        var t=a[1].split(":");
        t[2] = t[2].substring(0, 2);
        date = new Date(d[0],(d[1]-1),d[2],t[0],t[1],t[2]);

        var day = date.getDate();
        var monthIndex = date.getMonth();
        var year = date.getFullYear();

        return day + ' ' + monthNames[monthIndex] + ' ' + year;
}

/**
 * Take a string, parse is to find a float and return the price with the simbol of the currency
 */

function formatPrice(value){
    var price = parseFloat(value);
    price.toFixed(2);
    price = price + " 	\u20ac"
    return price;
}


/**
 * encodeData and decodeData are taken from here in order to avoid the problem of ' unescaped
 * src:http://stackoverflow.com/questions/75980/when-are-you-supposed-to-use-escape-instead-of-encodeuri-encodeuricomponent
 */
function encodeData(s){
    return encodeURIComponent(s).replace(/\-/g, "%2D").replace(/\_/g, "%5F").replace(/\./g, "%2E").replace(/\!/g, "%21").replace(/\~/g, "%7E").replace(/\*/g, "%2A").replace(/\'/g, "%27").replace(/\(/g, "%28").replace(/\)/g, "%29");
}

function decodeData(s){
    try{
        return decodeURIComponent(s.replace(/\%2D/g, "-").replace(/\%5F/g, "_").replace(/\%2E/g, ".").replace(/\%21/g, "!").replace(/\%7E/g, "~").replace(/\%2A/g, "*").replace(/\%27/g, "'").replace(/\%28/g, "(").replace(/\%29/g, ")"));
    }catch (e) {
    }
    return "";
}

