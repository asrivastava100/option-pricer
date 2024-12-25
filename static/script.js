let btnCalcOptionPrice = document.getElementById("calcOptionPrice")
let optionType = document.getElementById("optionType")
let maturity = document.getElementById("maturity")
let stockPrice = document.getElementById("stockPrice")
let strike = document.getElementById("strike")
let volatility = document.getElementById("volatility")
let riskFreeRate = document.getElementById("riskFreeRate")
let priceRes = document.getElementById("priceRes")
//fetch('api/priceCall?optionType=call&maturity=0.25&stockPrice=100&strike=95&volatility=0.5&riskFreeRate=0.01')
btnCalcOptionPrice.addEventListener("click",()=>{
    let requestText = 'api/priceBasicOption?optionType=' + optionType.value + "&maturity=" + maturity.value + "&stockPrice=" + stockPrice.value + "&strike=" + strike.value + "&volatility=" + volatility.value + "&riskFreeRate=" + riskFreeRate.value
    priceRes.value = ""
    fetch(requestText).then(res =>{
        if(res.status == 200){
            return res.json()
        } else {
            throw new error();

        }
    }).then(data=> priceRes.value = data)
    .catch(err=>console.log("fetch failed"))
})
