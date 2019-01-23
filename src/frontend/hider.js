import $ from 'jquery';
// import template from 'lodash.template';
import _ from 'underscore';
import LocalCollection from './localCollection';


var Hider = function(props) {
    var hiddenClass = props.type + '--hidden';
    var toggleSelector = '.js-toggle-' + props.type;
    var multiSelector = '.' + props.type;

    var localCollection = new LocalCollection({
        key: props.storageKey,
        callback: function(collection){
            applyLocalCollectionState();
        }
    });

    var placeholderItem = document.querySelector('#placeholder-item-template');
    if (!placeholderItem) {
        throw 'Placeholder template not found';
    }
    var placeholderItemTemplate = _.template(placeholderItem.innerHTML);


    function setItemState(itemId, itemHid, isHidden) {
        var $item = $('#' + props.type + '-' + itemId);

        if ($item.hasClass(hiddenClass) === isHidden) {
            return;
        }

        $item.toggleClass(hiddenClass, isHidden);

        var $placeholderItem;
        if (isHidden) {
            $placeholderItem = $(placeholderItemTemplate({
                id: itemId,
                hid: itemHid,
                label: props.placeholderLabel,
                type: props.type
            }));
            $placeholderItem.insertAfter($item);
        }
        else {
            $placeholderItem = $('#placeholder-' + props.type + '-' + itemId);
            $placeholderItem.remove();
        }
    }


    function applyLocalCollectionState() {
        $(multiSelector).each(function(){
            var $item = $(this);
            var itemId = $item.attr('data-id');
            var itemHid = $item.attr('data-hid');
            var isHidden = localCollection.check(itemId);

            setItemState(itemId, itemHid, isHidden);
        });
    }


    function onToggleClick(ev) {
        var $toggler = $(ev.target);
        var itemId = $toggler.attr('data-id');
        var itemHid = $toggler.attr('data-hid');
        var isHidden = localCollection.toggle(itemId);

        setItemState(itemId, itemHid, isHidden);
    }


    function destroy() {
        localCollection.destroy();
        $(document).off('.' + props.storageKey);
    }


    // Initialize
    applyLocalCollectionState();
    $(document).on('click.' + props.storageKey, toggleSelector, onToggleClick);

    return {
        destroy: destroy
    };
};


export default Hider;
