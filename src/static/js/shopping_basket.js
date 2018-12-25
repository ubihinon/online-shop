function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setCSRFHeader() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function addProductInBasket(product_id) {
    setCSRFHeader();
    $.ajax({
        url: $(`#addBasketButton-${product_id}`).attr('url'),
        type: 'PUT',
        data: {
            "products": [product_id]
        },
        success: function (result) {
            M.toast({html: 'Added to shopping basket!'});
        }
    });
}

function deleteProductFromBasket(basket_id, product_id) {
    setCSRFHeader();
    $.ajax({
        url: $(`#deleteBasketButton-${product_id}`).attr('url'),
        type: 'DELETE',
        success: function (result) {
            $('#product-' + product_id).remove();
        }
    });
}