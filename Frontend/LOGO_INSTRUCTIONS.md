# Logo Setup Instructions

## How to Add Your AiriQ Logo

1. **Place your logo image** in the `public` folder:
   ```
   Frontend/public/airiq-logo.png
   ```

2. **Supported formats:**
   - PNG (recommended)
   - JPG/JPEG
   - SVG

3. **Recommended size:**
   - 200x200px or larger
   - Square format works best
   - Transparent background preferred

4. **Update the filename** (if different):
   - Open `src/components/AiriQLogo.tsx`
   - Change `'/airiq-logo.png'` to your filename
   - Example: `'/my-logo.png'`

5. **The logo will automatically appear** in the header once you place the file!

## Current Setup

The logo component is configured to:
- Display at 100px size (adjustable)
- Show a placeholder if image not found
- Maintain aspect ratio
- Work with circular/square logos

## File Location

```
Frontend/
  └── public/
      └── airiq-logo.png  ← Place your logo here
```

