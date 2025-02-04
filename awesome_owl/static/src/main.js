import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(Playground, document.body, config));

// The function whenReady() returns a Promise resolved when the DOM is ready (if not ready yet, resolved directly otherwise).
// If called with a callback as argument, it executes it as soon as the DOM ready (or directly).

// this syntax: '() => function()' is called an 'arrow function'
// Arrow functions are often used for their brevity and because they don't have their own this context. Instead, they inherit this from the surrounding scope, which can be useful in certain situations (e.g., event handlers or callbacks).