
import pandas as pd

class ModelObject:
    def __init__(self, model,model_type,snowflake_model=True):
        self.model_type = model_type
        self.model_obj = model
        self.model = model
        self.snowflake_model = snowflake_model
    
    def get_model_artifacts(self, session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob):
        model_artifacts = {}
        new_model_object = self.get_model_object()
        model_artifacts['model_obj'] = new_model_object
        model_artifacts['hyper_parameters'] = self.get_hyper_parameters(new_model_object)
        model_artifacts['final_df'] = self.get_final_df(session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob)
        return model_artifacts
    
    def get_hyper_parameters(self,new_model_object):
        hyper_parameters = new_model_object.get_params()
        updated_hp = {key:eval(str(f'"{value}"')) if not value==None else value for (key,value) in hyper_parameters.items()}
        return updated_hp

    def get_model_object(self):

        ## To get the model object from pipeline
        if str(type(self.model_obj)).find("pipeline") >= 1 :
            ## returing the last step of the model pipeline
            last_step_index = len(self.model_obj.steps) - 1
            return self.get_model(self.model_obj.steps[last_step_index][1])
        
        return self.get_model(self.model_obj)
    
    def get_model(self,model):
        ## To get the model object snowflake xgboost
        if all([
                str(type(model)).find("snowflake") > 1,
                str(type(model)).find("xgboost") > 1
            ]):
            return model.to_xgboost()
        
        ## ## To get the model object snowflake lightgbm
        elif all([
                str(type(model)).find("snowflake") > 1,
                str(type(model)).find("lightgbm") > 1
            ]):
            return model.to_lightgbm()
                        
        ## To get the model object from default snowflake model
        elif str(type(model)).find("snowflake") > 1 :
            return model.to_sklearn()

        else:
            ## Default model object
            return model


    def get_final_df(self, session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob):
        if self.snowflake_model:
            return snowflake_df
        else:
            no_rows = x_test.shape[0] ; final_pandas_dataframe = None
            if y_prob is None or self.model_type == "regression":
                final_pandas_dataframe = pd.concat([x_test.reset_index(drop=True).iloc[:no_rows,:],
                                                    y_test.reset_index(drop=True).squeeze(),
                                                    y_pred.reset_index(drop=True).squeeze()
                                                    ],axis=1)
            elif isinstance(y_prob, pd.DataFrame):
                final_pandas_dataframe = pd.concat([x_test.reset_index(drop=True).iloc[:no_rows,:],
                                                    y_test.reset_index(drop=True).squeeze(),
                                                    y_pred.reset_index(drop=True).squeeze(),
                                                    y_prob.reset_index(drop=True).squeeze()
                                                    ],axis=1)

            final_pandas_dataframe_columns = final_pandas_dataframe.columns.to_list()
            return session.create_dataframe(final_pandas_dataframe,schema=final_pandas_dataframe_columns)

    


