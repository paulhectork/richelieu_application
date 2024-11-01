/**
 * color manipulation functions using
 * https://gka.github.io/chroma.js
 */

import chroma from 'chroma-js';

/**
 * functions to get random colors.
 * - Math.random() > 0.5 ? ... allows to chose between two different gradiens for variety
 * - toFixed(1) rounds to .1 => we yield a random color from
 *     a discrete scale made of 10 steps (0..0.9).
 */
export const randomColorLight = () =>
  Math.random() > 0.7  // 0.7 to have more pink
  ? chroma.mix("#8dc6af", "#67e5cc", Math.random().toFixed(1))
  : chroma.mix("#67e57e", "#e667ce", Math.random().toFixed(1));
export const randomColorDark = () =>
  Math.random() > 0.5
  ? chroma.mix("#700045", "#510708", Math.random().toFixed(1))
  : chroma.mix("#510b07", "#030191", Math.random().toFixed(1));

/**
 * dark blue to light green colorscale
 * @param {Number} ratio: float in 0..1 range
 */
export const colorScaleBlue = (ratio) =>
  chroma.scale(["#030191", "#67e5cc"]).mode("lrgb").correctLightness()(ratio);

/**
 * dark blue to light green colorscale
 * @param {Number} ratio: float in 0..1 range
 */
export const colorScaleRed = (ratio) =>
  chroma.scale(["#700045", "#f97282"]).mode("lrgb").correctLightness()(ratio);