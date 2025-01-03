let btnCalcOptionPrice = document.getElementById("calcOptionPrice")
let optionType = document.getElementById("optionType")
let maturity = document.getElementById("maturity")
let stockPrice = document.getElementById("stockPrice")
let strike = document.getElementById("strike")
let volatility = document.getElementById("volatility")
let riskFreeRate = document.getElementById("riskFreeRate")
let priceRes = document.getElementById("priceRes")
let isLong = document.getElementById("isLong")
let btnCalcMultiplePrices = document.getElementById("calcMultiplePrices")
let optionPriceContainer = document.getElementById("optionPriceContainer")
let optionPriceFunctionChart
let optionDeltaChart
let btnProcessMultipleOptions = document.getElementById("processMultipleOptions")
let optionPriceMultipleChart


//fetch('api/priceCall?optionType=call&maturity=0.25&stockPrice=100&strike=95&volatility=0.5&riskFreeRate=0.01')
btnCalcOptionPrice.addEventListener("click",()=>{
    let requestText = 'api/priceBasicOption?optionType=' + optionType.value + "&maturity=" + maturity.value + "&stockPrice=" + stockPrice.value + "&strike=" + strike.value + "&volatility=" + volatility.value + "&riskFreeRate=" + riskFreeRate.value + "&isLong=" + isLong.value
    priceRes.value = ""
    fetch(requestText).then(res =>{
        if(res.status == 200){
            return res.json()
        } else {
            throw new error();

        }
    }).then(data => priceRes.value = data)
    .catch(err=>console.log("fetch failed"))
})


function createOptionChart(chData){
    if(optionPriceFunctionChart !== undefined){
        optionPriceFunctionChart.destroy()
    }
    optionPriceFunctionChart = new Chart(document.getElementById("optionPriceFunction"),
    {
        type:"line",
        data:{
            labels:chData.stock_prices,
            datasets:[
                {
                    label:"Option Price",
                    data:chData.option_prices
                },
                {
                    label:"Terminal Payoff",
                    data:chData.terminal_values
                }
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Option Price vs Stock Price'
                }
            }

        }

    }

)

}

function createOptionDeltaChart(chData){
    if(optionDeltaChart !== undefined){
        optionDeltaChart.destroy()
    }
    optionDeltaChart = new Chart(document.getElementById("optionDelta"),
    {
        type:"line",
        data:{
            labels:chData.stock_prices,
            datasets:[
                {
                    label:"Option Delta",
                    data:chData.deltas
                }
                
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Option Delta vs Stock Price'
                }
            }

        }

    }

)

}

btnCalcMultiplePrices.addEventListener("click",()=>{
    let requestText = 'api/priceMultipleOptions?optionType=' + optionType.value + "&maturity=" + maturity.value + "&stockPrice=" + stockPrice.value + "&strike=" + strike.value + "&volatility=" + volatility.value + "&riskFreeRate=" + riskFreeRate.value + "&isLong=" + isLong.value
    fetch(requestText).then(res =>{
        if(res.status == 200){
            return res.json()
        } else {
            throw new error();

        }
    }).then(data => {
        createOptionChart(data)
        createOptionDeltaChart(data)
        optionPriceContainer.classList.remove("d-none")
})
    .catch(err=>console.log("fetch failed"))
})

btnProcessMultipleOptions.addEventListener("click", async () => {
    let optionTypeData = Array.from(document.getElementsByClassName("optionType")).map(x => x.value)
    let isLongData = Array.from(document.getElementsByClassName("isLong")).map(x => x.value)
    let strikeData = Array.from(document.getElementsByClassName("strike")).map(x => x.innerText)
    let maturity = document.getElementById("maturity").value
    let volatility = document.getElementById("volatility").value
    let stockPrice = document.getElementById("stockPrice").value
    let riskFreeRate = document.getElementById("riskFreeRate").value 
    let optionData = optionTypeData.map((x, idx) => {
        return {
            type: x,
            isLong: isLongData[idx],
            strike: strikeData[idx]
        }
    })
    console.log(optionType, isLong, strike)

    let response = await fetch('/api/pricePortfolio', {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            maturity,
            volatility,
            stockPrice,
            riskFreeRate,
            options: optionData
        }),
    })

    let responseJson = await response.json()
    createOptionChart(responseJson)


})

