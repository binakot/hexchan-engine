var RefPopup = function(props) {
    var POPUP_VERTICAL_OFFSET = 5;

    var popupIsVisible = false;


    function init() {
        document.addEventListener('mouseover', onMouseOver);
        document.addEventListener('mouseout', onMouseOut);
    }


    function destroy() {
        document.removeEventListener('mouseover', onMouseOver);
        document.removeEventListener('mouseout', onMouseOut);
    }


    function onMouseOver(ev) {
        if (ev.target.classList.contains('js-ref')) {
            var hid = ev.target.innerHTML.replace('&gt;&gt;', '');
            var url = ev.target.getAttribute('href').replace('#', '');
            var postEl = document.querySelector('.js-post[data-hid="' + hid + '"]');

            popupIsVisible = true;

            if (postEl) {
                showPopup(ev.target, hid, postEl.cloneNode(true));
            } else {
                $.get(url)
                    .done(function (res) {
                        showPopup(ev.target, hid, res);
                    })
                    .fail(function (err) {
                        console.error(err);
                    });
            }
        }
    }


    function onMouseOut(ev) {
        popupIsVisible = false;
        hidePopups();
    }


    function showPopup(target, hid, content) {
        if (popupIsVisible) {
            var targetBox = target.getBoundingClientRect();

            var popupEl = $('<div>')
                .html(content)
                .addClass('ref-popup js-ref-popup')
                .attr('data-hid', hid)
                .css({
                    top: targetBox.top + targetBox.height + POPUP_VERTICAL_OFFSET + window.pageYOffset,
                    left: 0
                });

            popupEl.find('.js-toggle-thread, .js-toggle-post').remove();

            $('.js-popup-container').append(popupEl);
        }
    }


    function hidePopups() {
        var popupEls = document.querySelectorAll('.js-ref-popup');
        for (var i =0; i < popupEls.length; i += 1) {
            popupEls[i].remove();
        }
    }


    init();
    return {
        destroy: destroy,
    };
};


var refPopup = new RefPopup();
