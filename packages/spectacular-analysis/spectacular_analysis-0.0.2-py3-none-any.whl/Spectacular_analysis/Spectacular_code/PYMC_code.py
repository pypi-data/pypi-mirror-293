#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Spectacular function cde


import numpy as np
import warnings
import pandas as pd
import pymc as pm
import arviz as az
import pickle

class dummy_variable:
    def __init__(self):
        self.columns_to_drop = ['survey_id', 'time_spent', 'page_id', 'participant_id']
        self.columns_to_encode = ['color', 'vitals_labs', 'gradient', 'graph', 'riskbox']
       
    
    def encode(self, survey_data):
        # First, drop the  columns
        survey_data = survey_data.drop(columns=self.columns_to_drop)
        
        # Then, encode the data
        encoded_data = pd.get_dummies(survey_data, columns=self.columns_to_encode)

        return encoded_data
    
class SpectacularModel:
    def __init__(self, initial_mu, initial_sigma):
        self.beta_names = ['beta_0', 'beta_grayscale', 'beta_monochromatic', 'beta_redorangeyellow', 'beta_viridis',
                           'beta_Gradient_stratified_label', 'beta_Gradient_equalwidth_label', 'beta_Gradient_stratified_no_label',
                           'beta_Gradient_tapered_no_label', 'beta_Gradient_equalwidth_no_label', 'beta_Graph_dashed',
                           'beta_Graph_equal_thickness', 'beta_Graph_incr_thickness', 'beta_riskbox_difference',
                           'beta_riskbox_relative', 'beta_riskbox_percent', 'beta_Vitals_chevron_black_show_abnormal',
                           'beta_Vitals_red_hide_abnormal', 'beta_Vitals_bold_show_abnormal', 'beta_Vitals_chevron_red_show_abnormal',
                           'beta_Vitals_none_show_abnormal', 'beta_Vitals_red_show_abnormal']
        
        self.mu = {name: initial_mu for name in self.beta_names}
        self.sigma = {name: initial_sigma for name in self.beta_names}
        self.sigma['beta_0'] = 10
        self.dummy_encoder = dummy_variable()

    def run_model(self, survey_data, num_samples=4000, tune=4000):
        survey_encode = self.dummy_encoder.encode(survey_data)
        with pm.Model() as logic_model:
            betas = {name: pm.Normal(name, mu=self.mu[name], sigma=self.sigma[name]) for name in self.beta_names}
            
            logits = pm.invlogit(sum(betas[name] * survey_encode[col].values 
                                     for name, col in zip(self.beta_names[1:], survey_encode.columns[:-1])) + betas['beta_0'])
            
            observed = pm.Bernoulli('y_obs', p=logits, observed=survey_encode['layout_selected'].values)
            
            trace = pm.sample(num_samples, tune=tune, chains=4, cores=4, target_accept=0.96, return_inferencedata=True)
        
        summary = az.summary(trace)
        
        new_mu = {}
        new_sigma = {}
        for param in self.beta_names:
            new_mu[param] = summary.loc[param, 'mean']
            new_sigma[param] = summary.loc[param, 'sd']
        
        print("Updated mu and sigma values:")
        for param in self.beta_names:
            print(f"{param}: mu = {new_mu[param]:.3f}, sigma = {new_sigma[param]:.3f}")

        probabilities = {}
        for param in self.beta_names:
            beta_mean = trace.posterior[param].mean().item()
            prob = 1 / (1 + np.exp(-beta_mean))
            probabilities[param] = prob
        
        # Update the priors for the next survey
        self.mu = new_mu
        self.sigma = new_sigma
              
        spectacular = {'probabilities': probabilities,'new_mu': new_mu,'new_sigma': new_sigma}
        
        with open('spectacular.pkl', 'wb') as fp:
            pickle.dump(spectacular, fp)
            print('dictionary saved successfully to file')
        
        

        return trace, new_mu, new_sigma, probabilities
    
    # Specify the Mu and the sigma
    # model = SpectacularModel(initial_mu=-4.151, initial_sigma=2)
    
    # Call the model that we made before and the survey that we want to run the model with
    # it autimaitcally updated if we want to run it for next survey
    #trace, new_mu, new_sigma, probabilities = model.run_model(survey)

