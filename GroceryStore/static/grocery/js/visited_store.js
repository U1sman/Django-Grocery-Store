document.addEventListener("DOMContentLoaded", () => {

    // Toggle Review Menu visibility
    const reviewButton = document.querySelector(".review_button");
    const reviewBox = document.querySelector(".review_box")

    function review_box_visible(){
        if (getComputedStyle(reviewBox).display == "none"){
            reviewButton.innerHTML = `<i class="fa-solid fa-xmark"></i>  Cancel`;
            reviewBox.style.display = "block";
        }
        else if (getComputedStyle(reviewBox).display == "block"){
            reviewButton.innerHTML = '<i class="fa-regular fa-comment"></i> Review';
            reviewBox.style.display = "none";
        }
    }
    reviewButton.onclick = review_box_visible;

    
    // Toggle Buy Button Row
    const productRows = document.querySelectorAll(".product_tr_row")
    let hoverEnabled = true;

    productRows.forEach((row)=>{
        const buyButtonRow = row.querySelector(".buy_button_row");
        // if (){
            function showRow(){
                if(hoverEnabled){
                    buyButtonRow.style.display = "block"; 
                    buyButtonRow.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
                }
            }
            function hideRow(){
                if(hoverEnabled){
                    buyButtonRow.style.display = "none"; 
                }
            }   

            row.addEventListener("mouseenter", showRow);

            row.addEventListener("mouseleave", hideRow);
        // }

    });


    const buyToggleButtons = document.querySelectorAll(".buy_button_toggle");
    // Toggle Buying Row
    buyToggleButtons.forEach((button)=>{
            button.addEventListener("click", ()=>{
                // Find the .product_tr_row where the button is located
                const productRow = button.closest(".product_tr_row");
                // Get the next sibling element, which should be the .buying_row
                const buying_row = productRow.nextElementSibling;

                if (window.getComputedStyle(buying_row).display === "none"){

                    buying_row.setAttribute(
                        "style",
                        "display: flex; justify-content: center; align-items:center; gap:20px;"

                    );
                    button.innerHTML = "CLOSE";

                }
                else {
                    buying_row.style.display = "none" 
                    button.innerHTML = "BUY"
                }
            })

    })

    const buyingRows = document.querySelectorAll(".buying_row");
    buyingRows.forEach((buyingRow)=>{
        const costDisplayer = buyingRow.querySelector(".cost_displayer");
        const buyingForm = buyingRow.querySelector(".buying_form");
        const quantityField = buyingForm.querySelector(".quantity_field_buy");

        const nearestProductRow = buyingRow.previousElementSibling;
        const salePrice = Number(nearestProductRow.querySelector("#saleprice_td").innerHTML);

        quantityField.addEventListener("input", ()=>{

            const quantity_bought = Number(quantityField.value);
            const cost = salePrice * quantity_bought;

            costDisplayer.innerHTML = `Cost: ${cost}`
            
        })
    })



});