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
  			blueDark: 'var(--blue-dark)',
  			blueMiddle: 'var(--blue-middle)',
  			blueSoft: 'var(--blue-soft)',
  			blueSupersoft: 'var(--blue-supersoft)',
			blueSky: 'var(--blue-sky)',
  			blueCharcoal: 'var(--blue-charcoal)',
  			slateDark: 'var(--slate-dark)',
  			slateMiddle: 'var(--slate-middle)',
  			slateSoft: 'var(--slate-soft)',
  			greenDark: 'var(--green-dark)',
  			greenMiddle: 'var(--green-middle)',
  			greenSoft: 'var(--green-soft)',
  			greenSupersoft: 'var(--green-supersoft)',
  			lime: 'var(--lime)',
  			yellowDark: 'var(--yellow-dark)',
  			yellowMiddle: 'var(--yellow-middle)',
  			yellowSoft: 'var(--yellow-soft)',
  			yellowSupersoft: 'var(--yellow-supersoft)',
  			grayDark: 'var(--gray-dark)',
  			grayMiddle: 'var(--gray-middle)',
  			graySoft: 'var(--gray-soft)',
  			graySupersoft: 'var(--gray-supersoft)',
  			silverMiddle: 'var(--silver-middle)',
  			silverSoft: 'var(--silver-soft)',
			silverTransparent: 'var(--silver-transparent)',
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
  		backgroundImage: {
  			'uk-pattern': 'url(/svg/uk-pattern-patterned.svg)'
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
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
