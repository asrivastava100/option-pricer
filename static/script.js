let btnCalcCallPrice = document.getElementById("calcCallPrice")
let optionType = document.getElementById("optionType")
let maturity = document.getElementById("maturity")
let stockPrice = document.getElementById("stockPrice")
let strike = document.getElementById("strike")
let volatility = document.getElementById("volatility")
let riskFreeRate = document.getElementById("riskFreeRate")
let callPriceRes = document.getElementById("callPriceRes")
//fetch('api/priceCall?optionType=call&maturity=0.25&stockPrice=100&strike=95&volatility=0.5&riskFreeRate=0.01')
btnCalcCallPrice.addEventListener("click",()=>{
    let requestText = 'api/priceCall?optionType=' + optionType.value + "&maturity=" + maturity.value + "&stockPrice=" + stockPrice.value + "&strike=" + strike.value + "&volatility=" + volatility.value + "&riskFreeRate=" + riskFreeRate.value
    callPriceRes.value = ""
    fetch(requestText).then(res =>{
        if(res.status = 200){
            return res.json()
        } else {
            throw new error();

        }
    }).then(data=> callPriceRes.value = data)
    .catch(err=>console.log("fetch failed"))
})
