import { useEffect } from "react";
import CheckIcon from '../../../../assets/icons/check.svg?react'


const URLValidator = ({ url, setValid }) => {

    const validFormats = {
        "deck": "https://www.moxfield.com/decks/",
        "binder": "https://www.moxfield.com/binders/",
    }

    const id = url.split("/").pop();
    const valid = Object.values(validFormats).some(format => url.startsWith(format)) && id.length > 5;
    const type = Object.keys(validFormats).find(format => url.startsWith(validFormats[format]));

    useEffect(() => {
        setValid(valid);
    }, [valid]);

    if (!url) return null;

    return (
        <div className="pt-3 text-muted small">
            {valid ? "  Valid " + type : "Invalid URL"}
        </div>
    )
}

export default URLValidator;