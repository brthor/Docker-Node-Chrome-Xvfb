/**
  * This file is intended to be copy/pasted into the browser console while
  * already logged in and on the build settings page for this repo.
  *
  * NOTE: Firefox is the only browser that can handle this script.
 */

var triggerButtons = document.querySelectorAll('button.Button__button___2lhyK.Button__variant-ghost-primary___1GaYs');

function main(index, count) {
    if (index >= count) {
        return;
    }

    console.log(`Triggered ${index} / ${count}`);

    var triggerButton = triggerButtons[index];

    triggerButton.click();
    setTimeout(() => main(++index, count), 25);
}

main(0, triggerButtons.length);