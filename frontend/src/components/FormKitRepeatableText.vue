<template>

  <!-- custom FormKit input for a repeatable text field
  
       props:
       * placeholder: the placeholder to display.
       * labelText: the text for the html label element
  
       partially adapted from:
       https://formkit.com/playground?fkv=latest&fileTab=Playground.vue&files=jc%5B%28%27name%21%27Playground.vue%27%7Eeditor%21%27%3CscripBsetupG%3FqfVvue%222%3FtokenV%40formkit%2Futils%2222U_%5E%5DS2%2F%2F+Iterating+over+this%3A2UiN%5E%26%5DS2UaddINQ%7B%7DZ%282+9.push%7B%26S%2922UrTINQ%7Be%7DZ%282*e.pqventDefault%7BS*UWQe.target.getAttribute%7BjSJ*9Q9.filter%7BiNZiN+%27%3A%3D%3D+WS*J%292LscriptG2%3CNplateG*%3COBtypeHlist3+v-modelH_s3G**%3COt6v-forHW+in+iNs36%3AWHW36%3AidHW36typeHtext36labelHEmail+Addqss36helpHediBme+to+geBstarted36%3Asections-schemaH%286*suffix4%286**%24elXaMattrs4%286***classX%24classes.rTM*jX%24idM*hqfX%23M*onClick4rTIN6**%29%2C6**childqnXRT%226*%296%2932**%2FG*LOtG*%3COB2**typeHbutton3+2**%40click.pqventHaddIN32*G**%2B+Add+Email2*LOtG*%3Cpq+wrap%3E%28%28+_s+%29%29LpqGLNplateG2%3CstyleG.formkit-rT+%282*position4absoluteY*left4calc%7B100%25+%2B+.5em%7DY*color4qdY*font-size4.75emY%292button+%282*align-self4flex-startY%292LstyleG%27%7Eadded%21true%29%5D*++2%5Cn3%5C%274%3A+62***Q%3D9iNs._Bt+G%3E2H%3D3J*console.log%7B%5B...9%5DSL%3C%2FM%22%2C6**NtemOFormKiQ8+S%7D2TemoveUconsBV+%29+from+%22WkeyX4%22Y%3B2Z8%3E+_valuej%22data-W%22qre%26token%7B%7D%3FimporB%28+%5EsQqf%7B%5B%01%5E%3F%26qj_ZYXWVUTSQONMLJHGB986432*_&imports=jc%28%27name%21%27ImpRtMap%27%7EeditR%21%27%28EDK59TDBK5B%400.8.4OB.Qm.js6D2D7%3FD%3D596cRe2cRe*G2G*dev2dev*themQ2themQ*i18n2i18n*inputs2inputs*N2N*rulQ2rulQ*G2G*J2J7HP%29P%27%29*762KCL.iF5Cjsdelivr.neFnpm%2FD6T%40LiF7%40%25LitVSsionInject%259%403O.Qm-browsS.jsA+HB3-sfc-loadSChttps%3A%2F%2Fcdn.DvueEP+AFt%2FGutilsH%5C%27JvalidationK%5C%21ALfRmkNobsSvSO%2FdisFDP%5CnQesRorSerTH%2CE%01TSRQPONLKJHGFEDCBA97652*_&css-framework=genesis
  -->



  <div class="form-field-input-wrapper">
    <ul class="repeatable-text-group list-invisible">
      <li v-for="[htmlId, val] in Object.entries(inputFields)">
        <label :for="htmlId" v-html="positionnedLabelText(htmlId)" hidden></label>
        <div class="input-wrapper">
          <input type="text"
                 :id="htmlId"
                 :name="htmlId"
                 :data-key="htmlId"
                 :placeholder="placeholder"
                 :value="val"
                 class="text-input"
                 @input="inputHandler"
          ></input>
          <div class="button-container">
            <UiButtonCross v-if="displayUiButtonCross(htmlId)"
                        type="button"
                        @click="popField(htmlId)"
                        @touchEnd="popField(htmlId)"
            ></UiButtonCross>
            <UiButtonPlus v-if="displayUiButtonPlus(htmlId)"
                        type="button"
                        @click="addField"
                        @touchEnd="addField"
            ></UiButtonPlus>
          </div>
        </div>
      </li>
    </ul>
  </div>

</template>


<script setup>
import { ref, onMounted } from "vue";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiButtonPlus from "@components/UiButtonPlus.vue";

/******************************************/

const props            = defineProps(["context"]);
const placeholder      = props.context.placeholder ? props.context.placeholder : "Écrire une valeur..."
const genericLabelText = props.context.labelText ? props.context.labelText : "Valeur";  // base value for the label, which will be augmented using `positionnedLabelText()`
const inputFields      = ref({});   // { <html id>: <value> }. this stores our data, while at the same time defining the HTML.

/******************************************/

/**
 * generate a unique name, html id...
 */
const makeId = () => `form-repeatable-text-${window.crypto.randomUUID()}`;

/**
 * take the generic value `labelText` and add `n°1`, `n°2`...
 * based on the position of the input in the input list.
 * @param {string} htmlId: the html ID and name of the current input
 */
 const positionnedLabelText = (htmlId) =>
  Object.keys(inputFields.value).length > 1
  ? `${genericLabelText} n°${Object.keys(inputFields.value).indexOf(htmlId) + 1}`
  : genericLabelText;

/**
 * add a field to the repeatable text field.
 */
const addField = () => {
  inputFields.value[makeId()] = undefined };

/**
 * remove a field from the repeatable text field based
 * on its html ID. this function handles the removal of
 * the `inputFields` entry, which is propagated to the
 * HTML (thanks to the @value attribute on the html <input>).
 * @param {string} htmlId: the html ID of the element to remove.
 */
const popField = (htmlId) => {
  if ( Object.keys(inputFields.value).includes(htmlId) ) {
    delete inputFields.value[htmlId]
  }
};

/**
 * reinitialize the input fields list.
 */
const reinitFields = () => {
  inputFields.value = {}; addField();  // remove all fields, add 1 empty
}

/**
 * handle the input by sending it to the formkit context.
 * @param {event} e
 */
function inputHandler(e) {
  inputFields.value[e.originalTarget.id] = e.srcElement.value;  // update `inputFields`
  props.context.node.input( Object.values(inputFields.value) );
}

/**
 * our repeatable input fields are contained in a list.
 * each `<li>` contains an `<input>` and two optional buttons
 * that can add/remove an input field.
 *
 * `displayUiButtonPlus` and `displayUiButtonCross` allows us
 * to control the display of the `UiButtonPlus` (add an input)
 * and `UiButtonCross` (remove an input) components:
 * - displayUiButtonPlus: UiButtonPlus is only present on the
 *   last <li> in the <ul>
 * - displayUiButtonCross: if there is only one `<li>` in the <ul>,
 *   UiButtonCross is not present.
 *
 * @param {string} htmlId: the ID of the input in the same `<li>`
 *   as the input button.
 *  */
const displayUiButtonPlus = (htmlId) =>
  Object.keys(inputFields.value).indexOf(htmlId)
  === Object.keys(inputFields.value).length - 1;

const displayUiButtonCross = (htmlId) =>
  Object.keys(inputFields.value).length > 1;

/******************************************/

onMounted(() => {
  addField();
})
</script>


<style scoped>
/*
ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
  margin-top: 0;
}
*/
label {
  font-weight: bold;
}
.input-wrapper {
  display: flex;
}
input {
  margin: .5% 0;
  flex-grow: 2;
  border: var(--cs-main-border);
}
.button-container > button {
  display: inline-table;
  width: 30px;
  height: 30px;
}
</style>
