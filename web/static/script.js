let maturity = document.getElementById("maturity")
let stockPrice = document.getElementById("stockPrice")
let volatility = document.getElementById("volatility")
let riskFreeRate = document.getElementById("riskFreeRate")
let optionPriceFunctionChart
let optionDeltaChart
let btnProcessMultipleOptions = document.getElementById("processMultipleOptions")
let btnDelete = document.getElementById("btnDeleteOption")
let btnAdd = document.getElementById("btnAddOption")
let optionTable = document.getElementById("optionTable")


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

btnProcessMultipleOptions.addEventListener("click", async () => {
    let optionTypeData = Array.from(document.getElementsByClassName("optionType")).map(x => x.value)
    let isLongData = Array.from(document.getElementsByClassName("isLong")).map(x => x.value)
    let strikeData = Array.from(document.getElementsByClassName("strike")).map(x => x.innerText)
    let priceOutput = Array.from(document.getElementsByClassName("price"))
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
    priceOutput.forEach((elem,idx)=>{
        elem.innerText = responseJson.current_option_price[idx]
    })
})

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
    let newRow = addRow("optionTable")
    let optTypeTd = addTd(newRow)
    let isLongTd = addTd(newRow)
    let strike = addTd(newRow)
    let price = addTd(newRow)

    let optTypeSelect = addSelect(optTypeTd,["optionType","form-select"])
    let optTypeOption1 = addOptForSelect(optTypeSelect,"call","Call")
    let optTypeOption2 = addOptForSelect(optTypeSelect,"put","Put")
    
    let isLongSelect = addSelect(isLongTd,["isLong","form-select"])
    let isLongOption1 = addOptForSelect(isLongSelect,"True","Long")
    let isLongOption2 = addOptForSelect(isLongSelect,"False","Short")
    
    strike.setAttribute("contenteditable","true")
    strike.classList.add("strike")
    price.classList.add("price")
    


})

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