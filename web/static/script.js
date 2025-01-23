let optionPriceFunctionChart
let optionDeltaChart
let btnProcessMultipleOptions = document.getElementById("processMultipleOptions")
let btnDelete = document.getElementById("btnDeleteOption")
let btnAdd = document.getElementById("btnAddOption")
let optionTable = document.getElementById("optionTable")
let optionProfitMultipleChart
let stockSimChart
let straddle = document.getElementById("straddle")
let bearSpread = document.getElementById("bearSpread")
let bullSpread = document.getElementById("bullSpread")


window.onload = setTimeout(() => priceAll(), 500);

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
                    data:chData.option_prices,
                    pointRadius:0,
                },
                {
                    label:"Terminal Payoff",
                    data:chData.terminal_values,
                    pointRadius:0,
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
                    data:chData.deltas,
                    pointRadius:0,
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

function createOptionProfitChart(chData){
    if(optionProfitMultipleChart !== undefined){
        optionProfitMultipleChart.destroy()
    }
    optionProfitMultipleChart = new Chart(document.getElementById("optionProfitMultipleChart"),
    {
        type:"line",
        data:{
            labels:chData.stock_prices,
            datasets:[
                {
                    label:"Profit",
                    data:chData.profit,
                    pointRadius:0,
                }
                
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Profit vs Stock Price'
                }
            }

        }

    }

)

}

function createStockSimChart(chData){
    if(stockSimChart !== undefined){
        stockSimChart.destroy()
    }
   
    stockSimChart = new Chart(document.getElementById("stockSimChart"),
    {
        type:"line",
        data:{
            labels:chData.time_axis,
            datasets: chData.stock_percentiles.map((x,i) => {
                return {
                    label:`${chData.percentiles[i]}%`,
                    data:x,
                    fill:"+1",
                    pointRadius:0,
                }

            })
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Percentiles of Risk Neutral GBM paths'
                },
                legend: {
                    display: true
                }
            }

        }

    }

)

}

async function showStockPriceChart(){

    let optionTypeData = Array.from(document.getElementsByClassName("optionTypeMC")).map(x => x.value)
    let isLongData = Array.from(document.getElementsByClassName("isLongMC")).map(x => x.value)
    let strikeData = Array.from(document.getElementsByClassName("strikeMC")).map(x => x.innerText)
    let priceOutput = Array.from(document.getElementsByClassName("priceMC"))
    let maturity = document.getElementById("maturityMC").value
    let volatility = parseFloat(document.getElementById("volatilityMC").value) / 100
    let stockPrice = document.getElementById("stockPriceMC").value
    let riskFreeRate = parseFloat(document.getElementById("riskFreeRateMC").value) / 100
    let optionData = optionTypeData.map((x, idx) => {
        return {
            type: x,
            isLong: isLongData[idx],
            strike: strikeData[idx]
        }
    })

    let response = await fetch('/api/stockPriceSim', {
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

    let chData = await response.json()

    priceOutput[0].innerText = chData.opt_price.toFixed(2)
    createStockSimChart(chData)

}

btnProcessMultipleOptions.addEventListener("click", priceAll)

async function priceAll() {
    let optionTypeData = Array.from(document.getElementsByClassName("optionType")).map(x => x.value)
    let isLongData = Array.from(document.getElementsByClassName("isLong")).map(x => x.value)
    let strikeData = Array.from(document.getElementsByClassName("strike")).map(x => x.innerText)
    let priceOutput = Array.from(document.getElementsByClassName("price"))
    let maturity = document.getElementById("maturity").value
    let volatility = parseFloat(document.getElementById("volatility").value) / 100
    let stockPrice = document.getElementById("stockPrice").value
    let riskFreeRate = parseFloat(document.getElementById("riskFreeRate").value) / 100
    let optionData = optionTypeData.map((x, idx) => {
        return {
            type: x,
            isLong: isLongData[idx],
            strike: strikeData[idx]
        }
    })

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
    createOptionDeltaChart(responseJson)
    createOptionProfitChart(responseJson)
    priceOutput.forEach((elem,idx)=>{
        elem.innerText = responseJson.current_option_price[idx].toFixed(2)
    })
}

function addRow(tblId){
    let tblRef = document.getElementById(tblId)
    let newRow = tblRef.insertRow(-1)
    return newRow
}

function addTd(row){
    let newTd = row.insertCell(-1)
    return newTd
}

function addSelect(tdElem, classesToAdd = []){
    let newSelect = document.createElement("select")
    tdElem.appendChild(newSelect)
    if(classesToAdd.length !== 0) {
        for(elem of classesToAdd){
            newSelect.classList.add(elem)
        }         
    } 
    return newSelect
}

function addOptForSelect(selectElem, val, txt){
    let opt1 = document.createElement("option")
    opt1.value = val
    opt1.text = txt
    selectElem.add(opt1)
    return opt1
}

btnAdd.addEventListener("click",()=>{
    addRowOptionTable()
})

function addRowOptionTable(){
    let newRow = addRow("optionTable")
    let optTypeTd = addTd(newRow)
    let isLongTd = addTd(newRow)
    let strike = addTd(newRow)
    let price = addTd(newRow)

    optTypeTd.classList.add('px-0', 'py-0')
    isLongTd.classList.add('px-0', 'py-0')

    let optTypeSelect = addSelect(optTypeTd,["optionType","form-select", "form-select-sm"])
    let optTypeOption1 = addOptForSelect(optTypeSelect,"call","Call")
    let optTypeOption2 = addOptForSelect(optTypeSelect,"put","Put")
    
    let isLongSelect = addSelect(isLongTd,["isLong","form-select", "form-select-sm"])
    let isLongOption1 = addOptForSelect(isLongSelect,"True","Long")
    let isLongOption2 = addOptForSelect(isLongSelect,"False","Short")
    
    strike.setAttribute("contenteditable","true")
    strike.classList.add("strike")
    price.classList.add("price")
    return {"rowID":newRow,
            "optTypeSelect":optTypeSelect,
            "isLongSelect":isLongSelect,
            "strike":strike,
            "price":price
    }
}

function deleteRow(tblId) {
    let tblRef = document.getElementById(tblId);
    let rowCount = tblRef.rows.length;
    if(rowCount !== 2){
        tblRef.deleteRow(rowCount -1);
    }
    return
}

btnDelete.addEventListener('click', ()=>{
    deleteRow("optionTable")
})

homePageLink.addEventListener("click", ()=>{
    showNavbarTab(0)
    priceAll()
})

stockPriceSimPageLink.addEventListener("click",()=>{
    showNavbarTab(1)
    showStockPriceChart()
})

function showNavbarTab(tab){
    let navLinks = Array.from(document.querySelectorAll('nav .nav-link'))
    let pages = Array.from(document.querySelectorAll('.pagePanel'))
    navLinks.forEach(x => x.classList.remove('active'))
    navLinks[tab].classList.add('active')
    pages.forEach(x => x.style.display = "None")
    pages[tab].style.display = 'Block'

}

function resetTable(tblId){
    let tblRef = document.getElementById(tblId)
    let rowCount = tblRef.rows.length;
    while(rowCount > 2){
        deleteRow(tblId)
        rowCount = rowCount - 1
    }
}

straddle.addEventListener("click",()=>{
    resetTable("optionTable")
    let optionTypeData = Array.from(document.getElementsByClassName("optionType")).map(x => x.value = "call")
    let isLongData = Array.from(document.getElementsByClassName("isLong")).map(x => x.value = "True")
    let strikeData = Array.from(document.getElementsByClassName("strike")).map(x => x.innerText = "96")
    let maturity = document.getElementById("maturity").value
    let volatility = parseFloat(document.getElementById("volatility").value) / 100
    let stockPrice = document.getElementById("stockPrice").value
    let riskFreeRate = parseFloat(document.getElementById("riskFreeRate").value) / 100
    let callOpt = addRowOptionTable()
    let putOpt = addRowOptionTable()
})