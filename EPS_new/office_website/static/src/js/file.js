window.onload = function myFunction()
{

    var y=document.getElementsByClassName('oe_currency_value');//get the element of class and show all the element

    var x = y.item(1).innerHTML //get the first item
    if (x == '0,000')
    {
        document.getElementById("jsproduct").style.display = 'none'; //marche

    }

}
$(document).ready(function ()
{
var elements = document.getElementsByClassName("product_price");
for(var i=0; i<elements.length; i++)
{
    var el= elements[i];
    console.log(el)
    var z = elements[i].getElementsByClassName('oe_currency_value');
    console.log(z)
    for (j = 0; j < z.length; j++)
    {
            var e = z.item(j).innerHTML
            if (e == '0,000')
                {
                    elements[i].style.visibility = 'hidden';
                 }
     }

}
});

