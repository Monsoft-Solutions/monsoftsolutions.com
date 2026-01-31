import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintPluginAstro from 'eslint-plugin-astro';

export default [
  // Ignore patterns
  {
    ignores: ['dist/', '.astro/', 'node_modules/', '.vercel/'],
  },

  // Base JavaScript recommended rules
  js.configs.recommended,

  // TypeScript rules
  ...tseslint.configs.recommended,

  // Astro recommended rules
  ...eslintPluginAstro.configs.recommended,

  // Accessibility rules for Astro
  ...eslintPluginAstro.configs['jsx-a11y-recommended'],

  // Custom rules
  {
    rules: {
      // TypeScript specific
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',

      // General
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },

  // Allow console in scripts (CLI utilities)
  {
    files: ['scripts/**/*.ts', 'scripts/**/*.js'],
    rules: {
      'no-console': 'off',
    },
  },
];
