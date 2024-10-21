/**
 * UI helpers
 */

import $ from "jquery";

/***************************************************/

/**
 * returns true if a click happens outside of element $(selector).
 *
 * @example:
 * $(document).on("click", (e) => {
 *   if ( clickOutside(e, ".hm-inner-wrapper") ) {
 *     $(document).off("click");
 *     emit('closeHomeModal');
 *   }
 * });
 *
 * @param {JQuery.Event} event : the jquery click event
 * @param {String} selector: the html selector
 * @returns {bool}
 */
export const clickOutside = (event, selector) =>
  ( !$(event.target).closest(selector).length && $(selector).is(":visible") );

/***************************************************/

/**
 * @components/Ui*.vue components as strings.
 * in some libraries (Leaflet), using vue components is tedious.
 * so we put their string equivalent here.
 */
export const uiButtonFilter =
  `<button>
    <svg width="80%"
         height="80%"
         viewBox="-2 -2 27 27"
         fill="none"
         xmlns="http://www.w3.org/2000/svg"
         aria-label="Filtrer les données. En cliquant ce bouton, il sera possible de cliquer les données. Le dessin vectoriel représente un filtre."
    >
      <title>Filtrer les données</title>
      <desc>En cliquant ce bouton, il sera possible de cliquer les données.
        Le dessin vectoriel représente un filtre.</desc>
      <path fill-rule="evenodd"
            clip-rule="evenodd"
            d="M15 10.5A3.502 3.502 0 0 0 18.355 8H21a1 1 0 1 0 0-2h-2.645a3.502 3.502 0 0 0-6.71 0H3a1 1 0 0 0 0 2h8.645A3.502 3.502 0 0 0 15 10.5zM3 16a1 1 0 1 0 0 2h2.145a3.502 3.502 0 0 0 6.71 0H21a1 1 0 1 0 0-2h-9.145a3.502 3.502 0 0 0-6.71 0H3z"
            fill="#000000"
      />
    </svg>
  </button>`;

export const uiButtonPlus =
  `<button class="button-cross">
    <svg width="100%"
         height="100%"
         viewBox="0 0 24 24"
         fill="none"
         xmlns="http://www.w3.org/2000/svg"
         aria-label="Voir plus d'informations. Cliquer sur ce
                     bouton donnera accès à plus d'informations"

    >
      <title>Voir plus d'informations</title>
      <desc>Cliquer sur ce bouton donnera accès à plus d'informations</desc>
      <path d="M4 12H20M12 4V20"
            stroke="none"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
      />
    </svg>
  </button>`;

export const uiButtonCross =
  `<button class="button-cross">
    <svg width="100%"
         height="100%"
         viewBox="0 0 24 24"
         fill="none"
         xmlns="http://www.w3.org/2000/svg"
         aria-label="Voir moins d'informations. Cliquer sur
                     ce bouton fermera un bloc donnant des informations"
    >
      <title>Voir moins d'informations</title>
      <desc>Cliquer sur ce bouton fermera un bloc donnant des informations.</desc>
      <path d="M19 5L4.99998 19M5.00001 5L19 19"
            stroke="none"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
      />
    </svg>
  </button>`;

export const uiButtonQuestion = `
  <button class="button-question">
  <!-- source: https://www.svgrepo.com/svg/438795/question-mark
       credits:  Cfpb Design System Icons
       license: public domain -->
  <svg fill="#000000"
       width="100%"
       height="100%"
       viewBox="-5.5 0 20 20"
       xmlns="http://www.w3.org/2000/svg"
       class="cf-icon-svg"
       aria-label="Pour plus d'explications: cliquer sur ce bouton vous donnera plus d'explications"
  >
    <title>Pour plus d'explications</title>
    <desc>Cliquer sur ce bouton vous donnera plus d'explications</desc>
    <path d="M7.987 5.653a4.536 4.536 0 0 1-.149 1.213 4.276 4.276 0 0 1-.389.958 5.186 5.186 0 0 1-.533.773c-.195.233-.386.454-.568.658l-.024.026c-.17.18-.328.353-.468.516a3.596 3.596 0 0 0-.4.567 2.832 2.832 0 0 0-.274.677 3.374 3.374 0 0 0-.099.858v.05a1.03 1.03 0 0 1-2.058 0v-.05a5.427 5.427 0 0 1 .167-1.385 4.92 4.92 0 0 1 .474-1.17 5.714 5.714 0 0 1 .63-.89c.158-.184.335-.38.525-.579.166-.187.34-.39.52-.603a3.108 3.108 0 0 0 .319-.464 2.236 2.236 0 0 0 .196-.495 2.466 2.466 0 0 0 .073-.66 1.891 1.891 0 0 0-.147-.762 1.944 1.944 0 0 0-.416-.633 1.917 1.917 0 0 0-.62-.418 1.758 1.758 0 0 0-.723-.144 1.823 1.823 0 0 0-.746.146 1.961 1.961 0 0 0-1.06 1.062 1.833 1.833 0 0 0-.146.747v.028a1.03 1.03 0 1 1-2.058 0v-.028a3.882 3.882 0 0 1 .314-1.56 4.017 4.017 0 0 1 2.135-2.139 3.866 3.866 0 0 1 1.561-.314 3.792 3.792 0 0 1 1.543.314A3.975 3.975 0 0 1 7.678 4.09a3.933 3.933 0 0 1 .31 1.563zm-2.738 9.81a1.337 1.337 0 0 1 0 1.033 1.338 1.338 0 0 1-.71.71l-.005.003a1.278 1.278 0 0 1-.505.103 1.338 1.338 0 0 1-1.244-.816 1.313 1.313 0 0 1 .284-1.451 1.396 1.396 0 0 1 .434-.283 1.346 1.346 0 0 1 .526-.105 1.284 1.284 0 0 1 .505.103l.005.003a1.404 1.404 0 0 1 .425.281 1.28 1.28 0 0 1 .285.418z"
    />
  </svg>
  </button>`;