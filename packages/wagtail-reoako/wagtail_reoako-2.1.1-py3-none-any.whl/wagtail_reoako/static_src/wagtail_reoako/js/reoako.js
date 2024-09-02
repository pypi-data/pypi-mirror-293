import { getSelectionText } from './DraftUtils';

const { React } = window;
const { draftail } = window;
const { Modifier } = window.DraftJS;
const { EditorState } = window.DraftJS;
const { $ } = window;

class ReoakoModalWorkflowSource extends React.Component {
    constructor(props) {
        super(props);
        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    browseApi(modal, jsonData) {
        /**
         * This is a basic reimplementation of Wagtail's in-built PAGE_CHOOSER_MODAL_ON_LOAD_HANDLER with all the
         * "page" specific functionality stripped out of it.
         */

        /* save initial page browser HTML, so that we can restore it if the search box gets cleared */
        const initialPageResultsHtml = $('.reoako-search-results', modal.body).html();

        /* Set up submissions of the search form to open in the modal. */
        modal.ajaxifyForm($('form.search-form', modal.body));

        /* Set up search-as-you-type behaviour on the search box */
        const searchUrl = $('form.search-form', modal.body).attr('action');

        let request;

        function search() {
          const query = $('#id_q', modal.body).val();
          if (query !== '') {
            request = $.ajax({
              url: searchUrl,
              data: {
                // eslint-disable-next-line id-length
                q: query,
              },
              success(data) {
                request = null;
                $('.reoako-search-results', modal.body).html(data);
                // eslint-disable-next-line @typescript-eslint/no-use-before-define
                ajaxifySearchResults();
              },
              error() {
                request = null;
              },
            });
          } else {
            /* search box is empty - restore original page browser HTML */
            $('.reoako-search-results', modal.body).html(initialPageResultsHtml);
            // eslint-disable-next-line @typescript-eslint/no-use-before-define
            ajaxifyBrowseResults();
          }
          return false;
        }

        // eslint-disable-next-line func-names
        $('#id_q', modal.body).on('input', function () {
          if (request) {
            request.abort();
          }
          clearTimeout($.data(this, 'timer'));
          const wait = setTimeout(search, 200);
          $(this).data('timer', wait);
        });

        /* Set up behaviour of choose-word links in the newly-loaded search results,
        to pass control back to the calling page */
        function ajaxifySearchResults() {
          // eslint-disable-next-line func-names
          $('.reoako-search-results a.reoako-choose-word', modal.body).on('click', function () {
            const pageData = $(this).data();
            modal.respond('wordChosen', pageData);
            modal.close();
            return false;
          });
        }

        /* Set up behaviour of reoako-choose-word links in the newly-loaded search results,
        to pass control back to the calling page */
        function ajaxifyBrowseResults() {
          /* Set up behaviour of reoako-choose-word links, to pass control back to the calling page */
          // eslint-disable-next-line func-names
          $('a.reoako-choose-word', modal.body).on('click', function () {
            const wordData = $(this).data();
            modal.respond('wordChosen', wordData);
            modal.close();
            return false;
          });
        }
        ajaxifyBrowseResults();
    }

    componentWillMount() {
        const { onClose, editorState } = this.props;
        $(document.body).on('hidden.bs.modal', this.onClose);

        const currentComponent = this;

        this.workflow = global.ModalWorkflow({
            url: '/admin/reoako-modal/',
            onload: {
                browse(modal, jsonData) {
                    const $searchForm = $('.search-form #id_q', modal.body);
                    $searchForm.attr('autocomplete', 'off');

                    currentComponent.browseApi(modal, jsonData);

                    const selectionText = getSelectionText(editorState);
                    if (selectionText) {
                        $searchForm.val(selectionText).trigger('input');
                    }
                    setTimeout(() => $searchForm.eq(0).focus(), 600);
                },
            },
            responses: {
                wordChosen: this.onChosen,
            },
            onError: (error) => {
                onClose();
            },
        });
    }

    componentWillUnmount() {
        this.workflow = null;
        $(document.body).off('hidden.bs.modal', this.onClose);
    }

    onChosen(data) {
        const { editorState, entityType, onComplete } = this.props;
        const selection = editorState.getSelection();
        const selectionSearchText = getSelectionText(editorState);
        const firstChar = selectionSearchText.charAt(0);
        let selectionText = data.reoakoTranslation;

        if (firstChar === firstChar.toUpperCase()) {
            selectionText = selectionText.charAt(0).toUpperCase() + selectionText.slice(1);
        };

        const content = editorState.getCurrentContent();
        const contentWithEntity = content.createEntity(
            entityType.type,
            'MUTABLE',
            data
        );
        const newEntityKey = contentWithEntity.getLastCreatedEntityKey();

        const newContent = Modifier.replaceText(content, selection, selectionText, null, newEntityKey);
        const nextState = EditorState.push(editorState, newContent, 'insert-characters');
        onComplete(nextState);
    }

    onClose() {
        const { onClose } = this.props;
        onClose();
    }

    render() {
        return null;
    }
}

const reoakoIcon = (
    <svg
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0, 0, 1024, 1024"
        width="1em"
        height="1em"
        style={{ verticalAlign: 'middle', marginRight: '2px' }}
    >
        <path
            d="M18.2822 114.286C18.2822 68.8406 55.1228 32 100.568 32H923.425C968.87 32 1005.71 68.8406 1005.71 114.286V813.714C1005.71 859.159 968.87 896 923.425 896H622.845L536.183 996.068C523.422 1010.8 500.564 1010.8 487.804 996.068L401.142 896H100.568C55.1228 896 18.2822 859.159 18.2822 813.714V672H443.593V524H443.59V430H443.593V301.438H509.406C565.752 301.438 593.024 325.719 593.024 370.344C593.024 414.75 565.752 437.062 509.856 437.062H444.59V513.188H514.815L602.265 672H710L611.957 497.875C664.472 476 693.547 431.594 693.547 370.344C693.547 281.312 632.918 224 528.113 224H346V671H18.2822V114.286Z"
            fill="currentColor"
        />
    </svg>
);

const Reoako = (props) => {
    const { entityKey, contentState, children } = props;
    const data = contentState.getEntity(entityKey).getData();
    // data: reoakoHeadword, reoakoId, reoakoTranslation

    return (
        <draftail.TooltipEntity
            { ...props }
            label={ `${ data.reoakoTranslation } (${ data.reoakoHeadword })` }
            icon={ reoakoIcon }
        >
            { children }{/* selected text */}
        </draftail.TooltipEntity>
    );
};

window.draftail.registerPlugin({
    type: 'REOAKO',
    source: ReoakoModalWorkflowSource,
    decorator: Reoako,
});
