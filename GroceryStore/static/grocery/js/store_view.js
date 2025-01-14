// Im not that good at js rn. So, sorry if this is bad js

const add_prdct_btn = document.querySelector(".add_btn");
const add_menu = document.querySelector(".add_menu");

function add_menu_visible(){
    if (getComputedStyle(add_menu).display == "none"){
        add_prdct_btn.innerHTML = "CLOSE MENU"
        add_menu.style.display = "block"
    }
    else if (getComputedStyle(add_menu).display == "block"){
        add_prdct_btn.innerHTML = "ADD NEW PRODUCT"
        add_menu.style.display = "none"
    }


};

add_prdct_btn.onclick = add_menu_visible;

const item_chooser = document.querySelector(".item_chooser")
const quantity_field = document.querySelector(".quantity_field");
const saleprice_field = document.querySelector(".saleprice_field");
const cost_price_display_p = document.querySelector(".cost_price_display_p");
const cost_price_display_t = document.querySelector(".cost_price_display_t");
const profit_margin_display_p = document.querySelector(".profit_margin_display_p");
const profit_margin_display_t = document.querySelector(".profit_margin_display_t");
let chosen_option_item_costprice = 0.00

// fetches the cost price dynamically and updates the cost price variable whenever the chosen option changes
// document.addEventListener("change", ()=>{
//     const chosen_option_item_string = item_chooser.value; // sent the value in the form of a string containing the cp and id directly insted of just the id so that i would not have to use an API to fetch the cost price
//     const regex = /(\d+\.\d{1,2}|\d+)\|(\d+)/;
//     const matches = chosen_option_item_string.match(regex);

//     if (matches) {
//         // The first captured group will be the cost price
//         chosen_option_item_costprice = matches[1];
//       }
//     else {
//         chosen_option_item_costprice = "N/A"
//     }

// });

function fetch_costprice_p(){
    const chosen_option_item_string = item_chooser.value; // sent the value in the form of a string containing the cp and id directly insted of just the id so that i would not have to use an API to fetch the cost price
    const regex = /(\d+\.\d{1,2}|\d+)\|(\d+)/;
    const matches = chosen_option_item_string.match(regex);

    if (matches) {
        // The first captured group will be the cost price
        return chosen_option_item_costprice = matches[1];
      }
    else {
        return chosen_option_item_costprice = "N/A";
    }
}

function update_costprice_display_p (){
    chosen_option_item_costprice = fetch_costprice_p();
    cost_price_display_p.innerHTML = `CostPrice(perunit): ${chosen_option_item_costprice}`;
      
}


// update cost_price_display_p on every change to the select menu
item_chooser.addEventListener("change", update_costprice_display_p);
// update cost_price_display_p by default when page loads
update_costprice_display_p()


function update_costprice_display_t (){
    chosen_option_item_costprice = fetch_costprice_p();
    let quantity_chosen = quantity_field.value 
    let total_costprice = chosen_option_item_costprice*quantity_chosen
    cost_price_display_t.innerHTML = `Total CostPrice: ${total_costprice}`;
}


item_chooser.addEventListener("change", update_costprice_display_t);
quantity_field.addEventListener("input", update_costprice_display_t);
update_costprice_display_t();


function update_profit_margin_display_p(){
    chosen_option_item_costprice = fetch_costprice_p();
    let saleprice_perunit = saleprice_field.value;
    
    let profit_margin_p = saleprice_perunit - chosen_option_item_costprice;

    profit_margin_display_p.innerHTML = `ProfitMargin(perunit): ${profit_margin_p}`;
}



item_chooser.addEventListener("change", update_profit_margin_display_p);
quantity_field.addEventListener("input", update_profit_margin_display_p);
saleprice_field.addEventListener("input", update_profit_margin_display_p)
update_profit_margin_display_p()


function update_profit_margin_display_t(){
    chosen_option_item_costprice = fetch_costprice_p();
    let quantity_chosen = quantity_field.value;
    let total_costprice = chosen_option_item_costprice*quantity_chosen;
    let saleprice_perunit = saleprice_field.value;
    let total_saleprice = saleprice_perunit*quantity_chosen;
    
    let profit_margin_t = total_saleprice - total_costprice;

    profit_margin_display_t.innerHTML = `Total ProfitMargin: ${profit_margin_t}`;
}

item_chooser.addEventListener("change", update_profit_margin_display_t);
quantity_field.addEventListener("input", update_profit_margin_display_t);
saleprice_field.addEventListener("input", update_profit_margin_display_t)
update_profit_margin_display_t()

document.addEventListener("DOMContentLoaded", () => {
    const product_rows = document.querySelectorAll(".product_tr_row")
    let hoverEnabled = true;

    // Toggle Edit Button Row
    product_rows.forEach((row)=>{
        const edit_button_row = row.querySelector(".edit_button_row");
        // if (){
            function showRow(){
                if(hoverEnabled){
                    edit_button_row.style.display = "block"; 
                    edit_button_row.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
                }
            }
            function hideRow(){
                if(hoverEnabled){
                    edit_button_row.style.display = "none"; 
                }
            }   

            row.addEventListener("mouseenter", showRow);

            row.addEventListener("mouseleave", hideRow);
        // }

    });

    const edit_buttons = document.querySelectorAll(".edit_button");
    // Toggle Editing Row
    edit_buttons.forEach((button)=>{
            button.addEventListener("click", ()=>{
                // Find the .product_tr_row where the button is located
                const productRow = button.closest(".product_tr_row");
                // Get the next sibling element, which should be the .editing_row
                const editing_row = productRow.nextElementSibling;

                if (window.getComputedStyle(editing_row).display === "none"){

                    editing_row.setAttribute(
                        "style",
                        "display: flex; justify-content: center; align-items:center; gap:10px;"

                    );
                    button.innerHTML = "CLOSE";

                }
                else {
                    editing_row.style.display = "none" 
                    button.innerHTML = "EDIT"
                }
            })

    })


    // Toggle Restock Button
    const restock_btns = document.querySelectorAll(".restock_btn")
        restock_btns.forEach((restock_btn)=>{
            restock_btn.addEventListener("click", ()=>{
                // Get the previous sibling of the restock button's parent, which is the .product_tr_row
                const currentEditingRow = restock_btn.closest(".editing_row");
                const closest_productrow = currentEditingRow.previousElementSibling;
                // Find the input field within the same row
                const quantity_field_increase = closest_productrow.querySelector(".quantity_field_increase");
                const quantity_td = closest_productrow.querySelector("#quantity_td");

                const restockSubmitBtn = currentEditingRow.querySelector(".restock_submit");
                const changePriceBtn = currentEditingRow.querySelector(".changeprice_btn");
                const deleteBtn = currentEditingRow.querySelector(".delete_btn");
                const costPriceDisplay_q = currentEditingRow.querySelector(".costprice_display_q");

                // Toggle display
                const currentDisplay = window.getComputedStyle(quantity_field_increase).display
                quantity_field_increase.style.display = currentDisplay === "none" ? "block" : "none";

                // Toggle display of quantity_td
                quantity_td.style.display = window.getComputedStyle(quantity_td).display === "block" ? "none" : "block";

                // Toggle innerHTML of restock_btn
                restock_btn.innerHTML = restock_btn.innerHTML === "RESTOCK" ? "CANCEL" : "RESTOCK";

                // Toggle display of restockSubmitBtn
                restockSubmitBtn.style.display = window.getComputedStyle(restockSubmitBtn).display === "none" ? "inline-block" : "none";

                // Toggle display of changePrice
                changePriceBtn.style.display = window.getComputedStyle(changePriceBtn).display === "none" ? "inline-block" : "none";

                // Toggle display of Delete
                deleteBtn.style.display = window.getComputedStyle(deleteBtn).display === "none" ? "inline-block" : "none";

                // Toggle display of costprice displayer
                costPriceDisplay_q.style.display = window.getComputedStyle(costPriceDisplay_q).display === "none" ? "inline-block" : "none";


                hoverEnabled = !hoverEnabled
            })
        });


    // Access the quantity field value and append that to the restock form when the restock submit button is clicked, affectively sending the value of the quantity increse field when the form is POSTED
    // This is needed because the quantity increase field is outside the restock form
    // Access the innerHTML(ie the name of the product) of the itemname_td field from the current row whose quantity is being edited and append that to the restock form when the restock submit button is clicked, affectively sending the itemName when the form is POSTED
    // This is needed because the name of the product whose quantity is being changed is needed
    const restockSubmitBtns = document.querySelectorAll(".restock_submit");
    restockSubmitBtns.forEach((restockSubmitBtn)=>{
        restockSubmitBtn.addEventListener("click", () => {
            const currentEditingRow = restockSubmitBtn.closest(".editing_row");
            const closestProductRow = currentEditingRow.previousElementSibling;
            const quantityFieldIncrease = closestProductRow.querySelector(".quantity_field_increase")

            const hiddenInput_quantity = document.createElement("input");
            hiddenInput_quantity.type = "hidden";
            hiddenInput_quantity.name = "quantity_field_increase";
            hiddenInput_quantity.value = quantityFieldIncrease.value;
            currentEditingRow.querySelector(".restock_form").appendChild(hiddenInput_quantity);

            const itemName = closestProductRow.querySelector("#itemname_td");
            const hiddenInput_itemName = document.createElement("input");
            hiddenInput_itemName.type = "hidden";
            hiddenInput_itemName.name = "item_name_quantity_increase";
            hiddenInput_itemName.value = itemName.innerHTML
            currentEditingRow.querySelector(".restock_form").appendChild(hiddenInput_itemName);
        });
    });

    // update the cost price displayer of the quantity of products being added to a product in the table
    const editingRows = document.querySelectorAll(".editing_row");
    editingRows.forEach((editingRow)=>{
        const nearestProductRow = editingRow.previousElementSibling;
        const quantityIncreaseField = nearestProductRow.querySelector(".quantity_field_increase");
        const costPriceDisplay_q = editingRow.querySelector(".costprice_display_q");
        const currentProductCostPrice = Number(nearestProductRow.querySelector("#costprice_td").innerHTML);

        quantityIncreaseField.addEventListener("input", ()=>{
            const addedQuantity = Number(quantityIncreaseField.value);
            const costPrice = currentProductCostPrice * addedQuantity;

            costPriceDisplay_q.innerHTML = `Costprice: ${costPrice}`
        })
    })


    // Toggle Changeprice Button
    const changeprice_btns = document.querySelectorAll(".changeprice_btn")
        changeprice_btns.forEach((changeprice_btn)=>{
            changeprice_btn.addEventListener("click", ()=>{
                // Get the previous sibling of the changeprice button's parent, which is the .product_tr_row
                const currentEditingRow = changeprice_btn.closest(".editing_row");
                const closest_productrow = currentEditingRow.previousElementSibling;
                // Find the input field within the same row
                const change_saleprice_field = closest_productrow.querySelector(".change_saleprice_field");
                const saleprice_td = closest_productrow.querySelector("#saleprice_td");

                const changepriceSubmitBtn = currentEditingRow.querySelector(".changeprice_submit");
                const restockBtn = currentEditingRow.querySelector(".restock_btn");
                const deleteBtn = currentEditingRow.querySelector(".delete_btn");

                // Toggle display
                const currentDisplay = window.getComputedStyle(change_saleprice_field).display
                change_saleprice_field.style.display = currentDisplay === "none" ? "block" : "none";

                // Toggle display of saleprice_td
                saleprice_td.style.display = window.getComputedStyle(saleprice_td).display === "block" ? "none" : "block";

                // Toggle innerHTML of changeprice_btn
                changeprice_btn.innerHTML = changeprice_btn.innerHTML === "CHANGE PRICE" ? "CANCEL" : "CHANGE PRICE";

                // Toggle display of changepriceSubmitBtn
                changepriceSubmitBtn.style.display = window.getComputedStyle(changepriceSubmitBtn).display === "none" ? "inline-block" : "none";

                // Toggle display of restockBtn
                restockBtn.style.display = window.getComputedStyle(restockBtn).display === "none" ? "inline-block" : "none";

                // Toggle display of Delete
                deleteBtn.style.display = window.getComputedStyle(deleteBtn).display === "none" ? "inline-block" : "none";

                hoverEnabled = !hoverEnabled
            })
        });

    // Adding the itemname and new sale price to the changeprice form
    const changepriceSubmitBtns = document.querySelectorAll(".changeprice_submit");
    changepriceSubmitBtns.forEach((changepriceSubmitBtn)=>{
        changepriceSubmitBtn.addEventListener("click", () => {
            const currentEditingRow = changepriceSubmitBtn.closest(".editing_row");
            const closestProductRow = currentEditingRow.previousElementSibling;
            const changeSalepriceField = closestProductRow.querySelector(".change_saleprice_field");

            const hiddenInput_saleprice = document.createElement("input");
            hiddenInput_saleprice.type = "hidden";
            hiddenInput_saleprice.name = "saleprice_field";
            hiddenInput_saleprice.value = changeSalepriceField.value;
            currentEditingRow.querySelector(".changeprice_form").appendChild(hiddenInput_saleprice);

            const itemName = closestProductRow.querySelector("#itemname_td");
            const hiddenInput_itemName = document.createElement("input");
            hiddenInput_itemName.type = "hidden";
            hiddenInput_itemName.name = "item_name_change_saleprice";
            hiddenInput_itemName.value = itemName.innerHTML
            currentEditingRow.querySelector(".changeprice_form").appendChild(hiddenInput_itemName);
        });
    });
    

});
