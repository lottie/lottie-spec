const Ajv = require('ajv/dist/2020');
const fs = require('fs');

const schema = require('../docs/lottie.schema.json');

const VALID_ANIMATIONS_DIR = './tests/animations/valid/';
const INVALID_ANIMATIONS_DIR = './tests/animations/invalid/';
const EXAMPLES_DIR = './docs/static/examples/';

const ajv = new Ajv();
const validate = ajv.compile(schema);

describe('run schema validation', () => {
    describe('example animations', () => {
        const exampleFiles = fs.readdirSync(EXAMPLES_DIR).map(file => EXAMPLES_DIR + file);

        exampleFiles.forEach((file) => {
            test(file, () => {
                const animation = fs.readFileSync(file, 'utf8');
                const valid = validate(JSON.parse(animation));
    
                expect(valid).toBe(true);
            });
        });
    });

    describe('valid animations', () => {
        const exampleFiles = fs.readdirSync(VALID_ANIMATIONS_DIR).map(file => VALID_ANIMATIONS_DIR + file);

        exampleFiles.forEach((file) => {
            test(file, () => {
                const animation = fs.readFileSync(file, 'utf8');
                const valid = validate(JSON.parse(animation));
    
                expect(valid).toBe(true);
            });
        });
    });

    describe('invalid animations', () => {
        const exampleFiles = fs.readdirSync(INVALID_ANIMATIONS_DIR).map(file => INVALID_ANIMATIONS_DIR + file);

        exampleFiles.forEach((file) => {
            test(file, () => {
                const animation = fs.readFileSync(file, 'utf8');
                const valid = validate(JSON.parse(animation));
    
                expect(valid).toBe(false);
            });
        });
    });
});
