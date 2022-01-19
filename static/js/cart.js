//To check if products exists in cart
// $(()=>{
//     if ($('.cart table tr#carttablerow').length <= 1) {
//         $('a.checkout').on('click', function(e){
//             e.preventDefault();
//         })
//     }
// })

//For add and subtract button
$(()=>{
    let prodSubTotalText = $('.prodOnlyTotal')
    let prodSubTotal = parseFloat(prodSubTotalText.text().slice(3))
    console.log(prodSubTotal)

    $('.initialbutton, .plusbutton, .minusbutton').on('click', function(e){
        e.preventDefault();
        let prod_id = $(this).attr('data-id');
        let prod_url = $(this).attr('data-url');
        let data_table_id = $(this).parent().parent().parent().attr('data-table-id');
        console.log(data_table_id)
        console.log(prod_id, prod_url)

        $.ajax({
            method: "POST",
            url : prod_url,
            data : {
                prod_id: prod_id,
                quantity: 1,
            },
            success: function(response){
                console.log(response.proqty, response.action)
                console.log(response.action)
                console.log(response.sub_total)
                console.log(response.cartproductcount)
                console.log(response.selling_price)
                if (response.action == 'subt' && response.proqty == 0){
                    $(`.datatableid${data_table_id}`).fadeOut();
                    $(`.mb${prod_id}`).fadeOut(1);
                    $(`.bt${prod_id}`).text(response.proqty).fadeOut(1);
                    $(`.pb${prod_id}`).fadeOut(1);
                    $(`.ib${prod_id}`).slideDown();
                    prodSubTotal -= response.selling_price
                    prodSubTotalSub = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalSub)
                    console.log(prodSubTotal)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(
                        ` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-sub-total="${key[1].sub_total}" data-delete-url="/delete-from-cart/" style="display: flex;justify-content: space-evenly;">
                            <div class="cartpopupprodimage">
                                <img src="${key[1].prod_image_url}" alt="" style="width: 100px; height: auto;">
                                <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                            </div>
                            <div class="cartpopupproddesc">
                                <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                                <p><strong> = Rs.${key[1].sub_total}</strong></p>
                            </div>
                            <div class="cartpopupprodremove">
                                <button class="popupDeleteCart"><i class="fa fa-trash" style="margin-top: 12px;"></i></button>
                            </div>
                          </div>`);
                    });
                    console.log('this is not cool bro')
                    $(`.cartpopupprod${response.product_id}`).fadeOut();
                    $('.cartproducttotal').text('Rs.'+popupsubtotal)
                    
                }else if(response.action == 'subt'){
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                    prodSubTotal -= response.selling_price
                    prodSubTotalSub = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalSub)
                    console.log(prodSubTotal)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-sub-total="${key[1].sub_total}" data-delete-url="/delete-from-cart/" style="display: flex;justify-content: space-evenly;">
                        <div class="cartpopupprodimage">
                            <img src="${key[1].prod_image_url}" alt="" style="width: 100px; height: auto;">
                            <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                        </div>
                        <div class="cartpopupproddesc">
                            <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                            <p><strong> = Rs.${key[1].sub_total}</strong></p>
                        </div>
                        <div class="cartpopupprodremove">
                        <button class="popupDeleteCart"><i class="fa fa-trash" style="margin-top: 12px;"></i></button>
                        </div>
                        </div>`);
                    });

                    $('.cartproducttotal').text('Rs.'+popupsubtotal)
                    let popupProdSubTotalText = $('.cartpopupprodsubtotal p strong')
                    let popupProdSubTotal = parseFloat(popupProdSubTotalText.text().slice(14))
                    console.log(cartproducts)


                    $('.popupDeleteCart').on('click', function(){
                        popupProdId = $(this).parent().parent().attr('data-prod-id');
                        popupProdUrl = $(this).parent().parent().attr('data-delete-url');
                        popupProdTotal = $(this).parent().parent().attr('data-sub-total');
                        console.log('hello gedey', popupProdTotal)
                        console.log(popupProdId, popupProdUrl, popupProdTotal);
                        $(`.datatableid${data_table_id}`).fadeOut();
                        $(`.mb${popupProdId}`).fadeOut(1);
                        $(`.bt${popupProdId}`).text(response.proqty).fadeOut(1);
                        $(`.pb${popupProdId}`).fadeOut(1);
                        $(`.ib${popupProdId}`).slideDown();
                        $.ajax({
                            method : "POST",
                            url : popupProdUrl,
                            data: {
                                prod_id: popupProdId
                            },
                            success: function(response){
                                $(`.cartpopupprod${response.rowId}`).fadeOut();
                                prodRealTotal = parseFloat($('.cartproducttotal').text().slice(3));
                                popFloat = parseFloat(popupProdTotal)
                                popupTotal = prodRealTotal - popFloat
                                $('.cartproducttotal').text('Rs.'+popupTotal)
                                $('.cartproductcount').text(response.cartproductcount);
                            },
                            error: function(response){
                                console.log('Error: ', response)
                            }
                        })
                    });


                }else if(response.action == 'add'){
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                    prodSubTotal += response.selling_price
                    prodSubTotalAdd = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalAdd)
                    console.log(prodSubTotal)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-sub-total="${key[1].sub_total}"  data-delete-url="/delete-from-cart/"  style="display: flex;justify-content: space-evenly;">
                        <div class="cartpopupprodimage">
                            <img src="${key[1].prod_image_url}" alt="" style="width: 100px; height: auto;">
                            <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                        </div>
                        <div class="cartpopupproddesc">
                            <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                            <p><strong> = Rs.${key[1].sub_total}</strong></p>
                        </div>
                        <div class="cartpopupprodremove">
                        <button class="popupDeleteCart"><i class="fa fa-trash" style="margin-top: 12px;"></i></button>
                        </div>
                        </div>`);
                    });
                    $('.cartproducttotal').text('Rs.'+popupsubtotal)

                    let popupProdSubTotalText = $('.cartpopupprodsubtotal p strong')
                    let popupProdSubTotal = parseFloat(popupProdSubTotalText.text().slice(14))
                    console.log(cartproducts)


                    $('.popupDeleteCart').on('click', function(){
                        popupProdId = $(this).parent().parent().attr('data-prod-id');
                        popupProdUrl = $(this).parent().parent().attr('data-delete-url');
                        popupProdTotal = $(this).parent().parent().attr('data-sub-total');
                        console.log(popupProdId, popupProdUrl, popupProdTotal);
                        $(`.datatableid${data_table_id}`).fadeOut();
                        $(`.mb${popupProdId}`).fadeOut(1);
                        $(`.bt${popupProdId}`).text(response.proqty).fadeOut(1);
                        $(`.pb${popupProdId}`).fadeOut(1);
                        $(`.ib${popupProdId}`).slideDown();
                        $.ajax({
                            method : "POST",
                            url : popupProdUrl,
                            data: {
                                prod_id: popupProdId
                            },
                            success: function(response){
                                $(`.cartpopupprod${response.rowId}`).fadeOut();
                                prodRealTotal = parseFloat($('.cartproducttotal').text().slice(3));
                                popFloat = parseFloat(popupProdTotal)
                                popupTotal = prodRealTotal - popFloat
                                $('.cartproducttotal').text('Rs.'+popupTotal)
                                $('.cartproductcount').text(response.cartproductcount);
                            },
                            error: function(response){
                                console.log('Error: ', response)
                            }
                        })
                    });
                }


                else{
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                }
                $('.cartproductcount').text(response.cartproductcount);
            },
            error: function(response){
                console.log('Error:', response)
            }
        })
    })

    $('.popupDeleteCart').on('click', function(){
        popupProdId = $(this).parent().parent().attr('data-prod-id');
        popupProdUrl = $(this).parent().parent().attr('data-delete-url');
        popupProdTotal = $(this).parent().parent().attr('data-prod-total');
        console.log(popupProdId, popupProdUrl, popupProdTotal);
        $(`.cartpopupprod${popupProdId}`).fadeOut();
        $.ajax({
            method : "POST",
            url : popupProdUrl,
            data: {
                prod_id: popupProdId
            },
            success: function(response){
                popupProdTotal -= response.prod_sub_total
                console.log(popupProdTotal)
                $('.cartproducttotal').text('Sub Total: Rs.'+popupProdTotal + '.0')
                $('.cartproductcount').text(response.cartproductcount);
            },
            error: function(response){
                console.log('Error: ', response)
            }
        })
    });

})








// For Remove Button
$(()=>{
    let prodSubTotalText = $('.prodOnlyTotal')
    let prodSubTotal = parseFloat(prodSubTotalText.text().slice(3))
    $('.dataTable').on('click', function(e){
        e.preventDefault();
        console.log('hello')
        const prodId = $(this).parent().parent().parent().parent().attr('data-table-id');
        const prodUrl = $(this).parent().parent().parent().parent().attr('data-table-url');
        console.log(prodId, prodUrl)
        $.ajax({
            method : "POST",
            url : prodUrl,
            data: {
                prod_id: prodId
            },
            success: function(response){
                $(`.datatableid${response.rowId}`).fadeOut();
                prodSubTotal -= response.prod_sub_total
                prodSubTotalAdd = `Rs.${prodSubTotal}.0`
                $('.prodOnlyTotal').text(prodSubTotalAdd)
                $('.cartproductcount').text(response.cartproductcount);
            },
            error: function(response){
                console.log('Error: ', response)
            }
        })
    })
});