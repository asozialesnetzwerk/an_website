// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt GNU-AGPL-3.0-or-later
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
"use strict";
(() => {
    const realAuthors = {};
    for (const child of elById("quote-list").children) {
        // put the quotes with their authors into an object
        realAuthors[
            (child as unknown as { value: string }).value.toLowerCase()
        ] = child
            .attributes
            .getNamedItem("data-author")
            .value;
    }

    const quoteInput = elById("quote-input") as HTMLInputElement;
    const realAuthorInput = elById("real-author-input") as HTMLInputElement;
    quoteInput.oninput = () => {
        const author = realAuthors[quoteInput.value.toLowerCase()];
        // when real author is found disable input and set the value
        realAuthorInput.disabled = !!author; // !! ≙ check of truthiness
        if (author) {
            realAuthorInput.value = author;
        }
    };
})();
// @license-end
