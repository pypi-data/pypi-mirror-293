import json
import loggerutility as logger
from .Image_TrainingPrediction import Image_TrainingPrediction
from .Text_TrainingPrediction import Text_TrainingPrediction
from flask import request
import weaviate

class Weaviate:
    modelParameter          = ""
    document_type           = ""
    train_Type              = ""

    def traindata(self,weaviate_jsondata, fileObj =""):

        if "modelParameter" in weaviate_jsondata and weaviate_jsondata["modelParameter"] != None:
            self.modelParameter = json.loads(weaviate_jsondata['modelParameter'])

        if "document_type" in self.modelParameter and (self.modelParameter["document_type"]).strip() != None:
            self.document_type = (self.modelParameter["document_type"]).capitalize().replace("-","_").strip()
            logger.log(f"\nWeaviate Hybrid class Document Type:::\t{self.document_type} \t{type(self.document_type)}","0")

        if "train_Type" in self.modelParameter and (self.modelParameter["train_Type"]).strip() != None:
            self.train_Type = (self.modelParameter["train_Type"]).capitalize().replace("-","_").strip()
            logger.log(f"\nWeaviate Hybrid class Train Type:::\t{self.train_Type} \t{type(self.train_Type)}","0")

        if self.document_type == "":
            text_TrainingPrediction = Text_TrainingPrediction()
            prediction_prediction_final = text_TrainingPrediction.traindata(weaviate_jsondata,'')
            logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
        else:
            if self.train_Type == "Img":
                image_TrainingPrediction = Image_TrainingPrediction()
                prediction_prediction_final = image_TrainingPrediction.imageTraining(weaviate_jsondata)
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            elif self.train_Type == "Text":
                text_TrainingPrediction = Text_TrainingPrediction()
                prediction_prediction_final = text_TrainingPrediction.traindata(weaviate_jsondata,'')
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            elif self.train_Type == "Both":
                text_TrainingPrediction = Text_TrainingPrediction()
                prediction_prediction_final = text_TrainingPrediction.traindata(weaviate_jsondata,'')
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")

                image_TrainingPrediction = Image_TrainingPrediction()
                prediction_prediction_final = image_TrainingPrediction.imageTraining(weaviate_jsondata)
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            else:
                logger.log(f"Invalid doctype:; {self.train_Type}")
        return prediction_prediction_final
    
    def getLookupData(self):

        weaviate_jsondata =  request.get_data('jsonData', None)
        weaviate_jsondata = json.loads(weaviate_jsondata[9:])
        logger.log(f"\nWeaviate hybrid class getLookupData() weaviate_json inside weaviate class:::\t{weaviate_jsondata} \t{type(weaviate_jsondata)}","0")

        if "modelParameter" in weaviate_jsondata and weaviate_jsondata["modelParameter"] != None:
            self.modelParameter = json.loads(weaviate_jsondata['modelParameter'])

        if "document_type" in self.modelParameter and (self.modelParameter["document_type"]).strip() != None:
            self.document_type = (self.modelParameter["document_type"]).capitalize().replace("-","_").strip()
            logger.log(f"\nWeaviate Hybrid class Document Type:::\t{self.document_type} \t{type(self.document_type)}","0")

        if "train_Type" in self.modelParameter and (self.modelParameter["train_Type"]).strip() != None:
            self.train_Type = (self.modelParameter["train_Type"]).capitalize().replace("-","_").strip()
            logger.log(f"\nWeaviate Hybrid class Train Type:::\t{self.train_Type} \t{type(self.train_Type)}","0")

        if self.document_type == "":
            text_TrainingPrediction = Text_TrainingPrediction()
            prediction_prediction_final = text_TrainingPrediction.getLookupData()
            logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
        else:
            if self.train_Type == "Img":
                image_TrainingPrediction = Image_TrainingPrediction()
                prediction_prediction_final = image_TrainingPrediction.Prediction_Image(weaviate_jsondata)
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            elif self.train_Type == "Text":
                text_TrainingPrediction = Text_TrainingPrediction()
                prediction_prediction_final = text_TrainingPrediction.getLookupData()
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            elif self.train_Type == "Both":
                text_TrainingPrediction = Text_TrainingPrediction()
                prediction_prediction_final = text_TrainingPrediction.getLookupData()
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")

                image_TrainingPrediction = Image_TrainingPrediction()
                prediction_prediction_final = image_TrainingPrediction.Prediction_Image(weaviate_jsondata)
                logger.log(f"prediction_prediction_final: {prediction_prediction_final}")
            else:
                logger.log(f"Invalid doctype:; {self.train_Type}")
        return prediction_prediction_final
    
    # Added by YashS on [ 29-08-24 ] for getting filtered schema list through [START]
    def getEnterpriseList(self):

        weaviate_jsondata =  request.get_data('jsonData', None)
        weaviate_jsondata = json.loads(weaviate_jsondata)['jsonData']
        logger.log(f"\nWeaviate hybrid class getLookupData() weaviate_json inside weaviate class:::\t{weaviate_jsondata} \t{type(weaviate_jsondata)}","0")

        if "server_url" in weaviate_jsondata and weaviate_jsondata["server_url"] != None:
            self.server_url = weaviate_jsondata["server_url"]
            logger.log(f"server_url  :::: {self.server_url} ")

        if "openAI_apiKey" in weaviate_jsondata and weaviate_jsondata["openAI_apiKey"] != None:
            self.openAI_apiKey = weaviate_jsondata["openAI_apiKey"]
            logger.log(f"openAI_apiKey  :::: {self.openAI_apiKey} ")

        if "enterprise" in weaviate_jsondata and weaviate_jsondata["enterprise"] != None:
            self.enterpriseName = weaviate_jsondata["enterprise"]
            logger.log(f"enterpriseName  :::: {self.enterpriseName} ")

        client = weaviate.Client(self.server_url, additional_headers={"X-OpenAI-Api-Key": self.openAI_apiKey})

        schema = client.schema.get()
        matching_classes = [cls['class'] for cls in schema['classes'] if cls['class'].lower().startswith(self.enterpriseName.lower())]
        
        logger.log(f"matching_classes  :::: {matching_classes} ")
        return matching_classes    
    # Added by YashS on [ 29-08-24 ] for getting filtered schema list through [END]

