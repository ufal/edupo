import type { Config } from "tailwindcss";

export default {
    darkMode: ["class"],
    content: [
		"./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/components/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/app/**/*.{js,ts,jsx,tsx,mdx}",
	],
	theme: {
		extend: {
			screens: {
				mobile: '480px',
				tablet: '768px',
				desktop: '1024px'
			},
			spacing: {
				docOffsetXBig: '1.25rem',
				docOffsetXSmall: '0.5rem',
				docOffsetY: '0.5rem'
			},
			colors: {
				crimsonRed: 'var(--crimson-red)',
				redDark: 'var(--red-dark)',
				redMiddle: 'var(--red-middle)',
				redSoft: 'var(--red-soft)',
				redSupersoft: 'var(--red-supersoft)',
				red200: 'var(--red-200)',
				red700: 'var(--red-700)',
				blueDark: 'var(--blue-dark)',
				blueMiddle: 'var(--blue-middle)',
				blueSoft: 'var(--blue-soft)',
				blueSupersoft: 'var(--blue-supersoft)',
				blueSky: 'var(--blue-sky)',
				blueCharcoal: 'var(--blue-charcoal)',
				slateDark: 'var(--slate-dark)',
				slateMiddle: 'var(--slate-middle)',
				slateSoft: 'var(--slate-soft)',
				slate200: 'var(--slate-200)',
				slate200Transparent: 'var(--slate-200-transparent)',
				slate300: 'var(--slate-300)',
				slate400: 'var(--slate-400)',
				slate700: 'var(--slate-700)',
				greenDark: 'var(--green-dark)',
				greenMiddle: 'var(--green-middle)',
				greenSoft: 'var(--green-soft)',
				greenSupersoft: 'var(--green-supersoft)',
				lime: 'var(--lime)',
				yellowDark: 'var(--yellow-dark)',
				yellowMiddle: 'var(--yellow-middle)',
				yellowSoft: 'var(--yellow-soft)',
				yellowSupersoft: 'var(--yellow-supersoft)',
				pink200: 'var(--pink-200)',
				pink200Transparent: 'var(--pink-200-transparent)',
				pink300: 'var(--pink-300)',
				pink600: 'var(--pink-600)',
				teal200: 'var(--teal-200)',
				teal200Transparent: 'var(--teal-200-transparent)',
				teal300: 'var(--teal-300)',
				teal600: 'var(--teal-600)',
				sky100: 'var(--sky-100)',
				sky200: 'var(--sky-200)',
				sky200Transparent: 'var(--sky-200-transparent)',
				sky300: 'var(--sky-300)',
				sky600: 'var(--sky-600)',
				sky800: 'var(--sky-800)',
				yellow200: 'var(--yellow-200)',
				yellow200Transparent: 'var(--yellow-200-transparent)',
				yellow300: 'var(--yellow-300)',
				yellow600: 'var(--yellow-600)',
				grayDark: 'var(--gray-dark)',
				grayMiddle: 'var(--gray-middle)',
				graySoft: 'var(--gray-soft)',
				graySupersoft: 'var(--gray-supersoft)',
				silverMiddle: 'var(--silver-middle)',
				silverSoft: 'var(--silver-soft)',
				silverTransparent: 'var(--silver-transparent)',
				zinc100: 'var(--zinc-100)',
				zinc200: 'var(--zinc-200)',
				black: 'var(--black)',
				blackSoft: 'var(--black-soft)',
				creamy: 'var(--creamy)',
				background: 'var(--background)',
				foreground: 'var(--foreground)',
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				}
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out'
			}
		}
	},
	safelist: [
		'bg-pink200', 'bg-pink200Transparent', 'bg-pink300', 'text-pink600',
		'bg-teal200', 'bg-teal200Transparent', 'bg-teal300', 'text-teal600',
		'bg-sky200', 'bg-sky200Transparent', 'bg-sky300', 'text-sky600',
		'bg-yellow200', 'bg-yellow200Transparent', 'bg-yellow300', 'text-yellow600',
		'slate200Transparent'
	  ],
	plugins: [require("tailwindcss-animate")],
} satisfies Config;
