import "@plugins/modernizr.js";

/**
 * static variables that are globally available to the app
 * and that are exposed/usable by th client (=> more permissive
 * than constants defined in `vite.config.js`)
 */

/**
 * is this a touchable browser?
 */
export const hasTouch = Modernizr.touchevents || Modernizr.pointerevents;

/**
 * listen to just click on non-touchscreen,
 * click+touchend on devices with touchscreen.
 *
 * see: https://web.dev/articles/mobile-touchandmouse
 */
export const clickOrTouchEvent = hasTouch ? "click touchend" : "click";