/*
 * wood.sl: a wood texture shader
 *
 * (c) Copyright 1990, 1995 by Aptech Systems, Inc.
 * All Rights Reserved.
 *
 * This code is based on the original wood shader from "The
 * RenderMan Companion" by Steve Upstill.  This version of the
 * shader has been modified to use the filtered noise function
 * and to add a few more controls.
 *
 * The original shader is (c) Copyright 1988 Pixar.
 * All Rights Reserved.
 */

surface
wood(
  /* light wood color */
  color C1 = color (0.5, 0.2, 0.07);
  /* dark wood color */
  color C2 = color (0.15, 0.08, 0.03);
  /* specular color */
  color spec = color (0.5, 0.5, 0.5);
  /* ambient intensity */
  float Ka = 0.2;
  /* diffuse intensity */
  float Kd = 0.8;
  /* specular intensity */
  float Ks = 0.2;
  /* specular roughness */
  float roughness = 0.1;
  /* scale of the texture */
  float scale = 1;
  /* ring thickness */
  float ring_thickness = 10;
  /* amount of waviness in the grain */
  float wavy = 0.1;
  /* amount of noise to add to the texture */
  float noise_amp = 0.1;
  /* frequency of the noise */
  float noise_freq = 2;
  )
{
  point PP;
  float r, r2, in_ring;
  float f;
  color Ct;
  
  /* transform the point to texture space */
  PP = transform("shader", P);
  PP *= scale;

  /* give the grain a wavy appearance */
  PP[0] += wavy * snoise(PP);

  /* calculate the radius from the center */
  r = sqrt(PP[0]*PP[0] + PP[1]*PP[1]);

  /* add some noise to the radius */
  r += noise_amp * snoise(PP * noise_freq);

  /* determine the ring based on the radius */
  r2 = r * ring_thickness;
  in_ring = mod(r2, 1);
  
  /* use a smoothstep to make the transition between rings */
  f = smoothstep(0.4, 0.6, in_ring);

  /* mix the two colors based on the ring pattern */
  Ct = mix(C1, C2, f);

  /* set the opacity */
  Oi = Os;

  /* calculate the final color with lighting */
  Ci = Oi * Ct * (Ka*ambient() + Kd*diffuse(normalize(N))) +
       spec * Ks*specular(normalize(N),-normalize(I),roughness);
}