import js from '@eslint/js';
import globals from 'globals';

export default [
  {
    files: ['scripts/**/*.js'],
    languageOptions: { globals: globals.browser },
    rules: js.configs.recommended.rules,
  },
];